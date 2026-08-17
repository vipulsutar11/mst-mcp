# pyrefly: ignore [missing-import]
from mcp.server import MCPServer
import os

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


import sys

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