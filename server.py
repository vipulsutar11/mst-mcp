# pyrefly: ignore [missing-import]
from mcp.server import MCPServer
from mcp.types import Resource
import os
import sys

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


@mcp.list_resources()
def list_resources() -> list[Resource]:
    """
    Lists all documentation files as MCP resources.
    """
    if not os.path.exists(DOCS_DIR):
        return []
    resources = []
    for filename in os.listdir(DOCS_DIR):
        if os.path.isfile(os.path.join(DOCS_DIR, filename)):
            resources.append(
                Resource(
                    uri=f"docs://{filename}",
                    name=filename,
                    mimeType="text/plain",
                    description=f"Documentation about {os.path.splitext(filename)[0]}"
                )
            )
    return resources


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


if __name__ == "__main__":
    if sys.stdin.isatty():
        print("==================================================")
        print("MST-MCP Server")
        print("==================================================")
        print("This is a Model Context Protocol (MCP) server that communicates via STDIO.")
        print("It is designed to be run by an MCP client (such as Claude Desktop or Cursor).")
        print("==================================================")
    else:
        mcp.run()