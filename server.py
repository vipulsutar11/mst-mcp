# pyrefly: ignore [missing-import]
from mcp.server import MCPServer
# pyrefly: ignore [missing-import]
from mcp.types import Resource
import os
import sys
from dotenv import load_dotenv

load_dotenv()

mcp = MCPServer("MST-MCP")

DOCS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Docuements")


@mcp.resource("docs://{filename}")
def get_doc_resource(filename: str) -> str:
    """
    Retrieves the contents of a documentation resource by its filename.
    """
    safe_filename = os.path.basename(filename)
    filepath = os.path.join(DOCS_DIR, safe_filename)
    
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Document {safe_filename} not found.")
        
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()


@mcp.tool()
def list_documents() -> list[str]:
    """
    Lists the filenames of all available documentation files in the server.
    """
    if not os.path.exists(DOCS_DIR):
        return []
    return [f for f in os.listdir(DOCS_DIR) if os.path.isfile(os.path.join(DOCS_DIR, f))]


@mcp.tool()
def read_document(filename: str) -> str:
    """
    Reads and returns the contents of a specific documentation file.

    Args:
        filename: The exact name of the file to read (e.g., 'SDK.txt').
    """
    safe_filename = os.path.basename(filename)
    filepath = os.path.join(DOCS_DIR, safe_filename)
    
    if not os.path.exists(filepath):
        return f"Error: Document '{filename}' not found."
        
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()


@mcp.tool()
def search_documents(query: str) -> dict[str, list[str]]:
    """
    Searches for a keyword or query inside all documents and returns matching lines with line numbers.

    Args:
        query: The search term or keyword to find.
    """
    results = {}
    if not os.path.exists(DOCS_DIR):
        return results
        
    query_lower = query.lower()
    for filename in os.listdir(DOCS_DIR):
        filepath = os.path.join(DOCS_DIR, filename)
        if os.path.isfile(filepath):
            matching_lines = []
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    for i, line in enumerate(f, 1):
                        if query_lower in line.lower():
                            matching_lines.append(f"Line {i}: {line.strip()}")
            except Exception:
                continue
            if matching_lines:
                results[filename] = matching_lines
                
    return results


# Create Starlette app for SSE transport
from starlette.applications import Starlette
from starlette.routing import Route, Mount
from starlette.responses import RedirectResponse, JSONResponse
# pyrefly: ignore [missing-import]
from mcp.server.sse import SseServerTransport

# Configuration for OAuth (Use environment variables or secure defaults)
CLIENT_ID = os.environ.get("OAUTH_CLIENT_ID", "mst-mcp-client")
CLIENT_SECRET = os.environ.get("OAUTH_CLIENT_SECRET", "mst-mcp-secret")

# Simple in-memory storage for authorization codes and access tokens
auth_codes = set()
access_tokens = set()

sse = SseServerTransport("/messages/")

async def handle_authorize(request):
    params = request.query_params
    client_id = params.get("client_id")
    redirect_uri = params.get("redirect_uri")
    state = params.get("state")
    
    if client_id != CLIENT_ID:
        return JSONResponse({"error": "invalid_client"}, status_code=400)
    
    # Generate a temporary authorization code
    code = "auth_code_" + os.urandom(8).hex()
    auth_codes.add(code)
    
    # Redirect back to Claude with the code and state
    callback_url = f"{redirect_uri}?code={code}"
    if state:
        callback_url += f"&state={state}"
        
    return RedirectResponse(url=callback_url)

async def handle_token(request):
    form_data = await request.form()
    client_id = form_data.get("client_id")
    client_secret = form_data.get("client_secret")
    code = form_data.get("code")
    
    if client_id != CLIENT_ID or client_secret != CLIENT_SECRET or code not in auth_codes:
        return JSONResponse({"error": "invalid_grant"}, status_code=400)
    
    # Clean up authorization code and issue access token
    auth_codes.remove(code)
    token = "token_" + os.urandom(16).hex()
    access_tokens.add(token)
    
    return JSONResponse({
        "access_token": token,
        "token_type": "Bearer"
    })

async def handle_protected_resource(request):
    base_url = str(request.base_url).rstrip('/')
    return JSONResponse({
        "resource": base_url,
        "authorization_servers": [
            base_url
        ],
        "scopes_supported": [
            "mcp"
        ],
        "bearer_methods_supported": [
            "header"
        ]
    })

async def handle_authorization_server(request):
    base_url = str(request.base_url).rstrip('/')
    return JSONResponse({
        "issuer": base_url,
        "authorization_endpoint": f"{base_url}/authorize",
        "token_endpoint": f"{base_url}/token",
        "scopes_supported": ["mcp"],
        "response_types_supported": ["code"],
        "grant_types_supported": ["authorization_code"],
        "code_challenge_methods_supported": ["S256"]
    })

async def handle_sse(request):
    # Verify access token
    auth_header = request.headers.get("Authorization")
    base_url = str(request.base_url).rstrip('/')
    if not auth_header or not auth_header.startswith("Bearer "):
        return JSONResponse(
            {"error": "unauthorized"}, 
            status_code=401,
            headers={
                "WWW-Authenticate": f'Bearer resource_metadata="{base_url}/.well-known/oauth-protected-resource"'
            }
        )
        
    token = auth_header.split(" ")[1]
    if token not in access_tokens:
        return JSONResponse(
            {"error": "forbidden"}, 
            status_code=403,
            headers={
                "WWW-Authenticate": f'Bearer resource_metadata="{base_url}/.well-known/oauth-protected-resource"'
            }
        )

    if request.method == "POST":
        return await sse.handle_post_message(request)

    async with sse.connect_sse(
        request.scope, request.receive, request._send
    ) as streams:
        await mcp.run(
            streams[0],
            streams[1],
            mcp.create_initialization_options(),
        )

app = Starlette(
    debug=True,
    routes=[
        Route("/.well-known/oauth-protected-resource", endpoint=handle_protected_resource, methods=["GET"]),
        Route("/.well-known/oauth-authorization-server", endpoint=handle_authorization_server, methods=["GET"]),
        Route("/authorize", endpoint=handle_authorize, methods=["GET"]),
        Route("/token", endpoint=handle_token, methods=["POST"]),
        Route("/sse", endpoint=handle_sse, methods=["GET", "POST"]),
        Mount("/messages/", app=sse.handle_post_message),
    ],
)


if __name__ == "__main__":
    port_env = os.environ.get("PORT")
    if port_env:
        import uvicorn
        port = int(port_env)
        print(f"Starting SSE MCP server on port {port}...")
        print(f"OAuth Client ID configured: {CLIENT_ID}")
        print(f"OAuth Client Secret configured: {CLIENT_SECRET}")
        uvicorn.run("server:app", host="0.0.0.0", port=port)
    elif sys.stdin.isatty():
        print("==================================================")
        print("MST-MCP Server")
        print("==================================================")
        print("This is a Model Context Protocol (MCP) server that communicates via STDIO.")
        print("It is designed to be run by an MCP client (such as Claude Desktop or Cursor).")
        print("==================================================")
    else:
        mcp.run()
