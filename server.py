# pyrefly: ignore [missing-import]
from mcp.types import Resource, Icon
# pyrefly: ignore [missing-import]
from mcp.server import MCPServer
import os
import sys
from dotenv import load_dotenv

load_dotenv()

# PNG Base64 encoded icon string to serve as local data URI
ICON_BASE64 = (
    "data:image/png;base64,"
    "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"
)

mcp = MCPServer(
    name="MST-MCP",
    version="1.0.0",
    icons=[
        Icon(
            src=ICON_BASE64,
            sizes=["512x512"],
            mime_type="image/png"
        )
    ]
)




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
from starlette.responses import RedirectResponse, JSONResponse, FileResponse
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
    
async def handle_authorize(request):
    params = request.query_params
    client_id = params.get("client_id")
    redirect_uri = params.get("redirect_uri")
    state = params.get("state")
    
    # Strictly validate against the environment variable CLIENT_ID (loaded from .env / Render env)
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
    # Try parsing client credentials from Basic Auth header first
    auth_header = request.headers.get("Authorization")
    client_id = None
    client_secret = None
    if auth_header and auth_header.startswith("Basic "):
        import base64
        try:
            decoded = base64.b64decode(auth_header.split(" ")[1]).decode("utf-8")
            client_id, client_secret = decoded.split(":", 1)
        except Exception:
            pass

    form_data = await request.form()
    if not client_id:
        client_id = form_data.get("client_id")
    if not client_secret:
        client_secret = form_data.get("client_secret")
    code = form_data.get("code")
    
    # Strictly validate against environmental CLIENT_ID and CLIENT_SECRET
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
    base_url = "https://mst-mcp.onrender.com"
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
    base_url = "https://mst-mcp.onrender.com"
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
    # Verify access token bypassed for testing direct Claude connection
    # auth_header = request.headers.get("Authorization")
    # base_url = "https://mst-mcp.onrender.com"
    # if not auth_header or not auth_header.startswith("Bearer "):
    #     return JSONResponse(
    #         {"error": "unauthorized"}, 
    #         status_code=401,
    #         headers={
    #             "WWW-Authenticate": f'Bearer resource_metadata="{base_url}/.well-known/oauth-protected-resource"'
    #         }
    #     )
    #     
    # token = auth_header.split(" ")[1]
    # if token not in access_tokens:
    #     return JSONResponse(
    #         {"error": "forbidden"}, 
    #         status_code=403,
    #         headers={
    #             "WWW-Authenticate": f'Bearer resource_metadata="{base_url}/.well-known/oauth-protected-resource"'
    #         }
    #     )


    if request.method == "POST":
        from starlette.responses import Response
        await sse.handle_post_message(request.scope, request.receive, request._send)
        return Response()

    async with sse.connect_sse(
        request.scope, request.receive, request._send
    ) as streams:
        await mcp._lowlevel_server.run(
            streams[0],
            streams[1],
            mcp._lowlevel_server.create_initialization_options(),
        )
    from starlette.responses import Response
    return Response()

async def handle_health(request):
    return JSONResponse({"status": "healthy", "server": "MST-MCP"})

async def handle_favicon(request):
    icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "icon.png")
    if os.path.exists(icon_path):
        return FileResponse(icon_path, media_type="image/png")
    return JSONResponse({"error": "Icon not found"}, status_code=404)

app = Starlette(
    debug=True,
    routes=[
        Route("/", endpoint=handle_health, methods=["GET"]),
        Route("/favicon.ico", endpoint=handle_favicon, methods=["GET"]),
        Route("/favicon.png", endpoint=handle_favicon, methods=["GET"]),
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
        uvicorn.run(
            "server:app",
            host="0.0.0.0",
            port=port,
            proxy_headers=True,
            forwarded_allow_ips="*"
        )
    elif sys.stdin.isatty():
        print("==================================================")
        print("MST-MCP Server")
        print("==================================================")
        print("This is a Model Context Protocol (MCP) server that communicates via STDIO.")
        print("It is designed to be run by an MCP client (such as Claude Desktop or Cursor).")
        print("==================================================")
    else:
        mcp.run()
