# MST-MCP Server

An MCP (Model Context Protocol) server designed for the MST Chain ecosystem. This server provides tools and resources to access MST Chain documentation, smart contract deployment guides, gas, EVM details, transactions, and network validator structures.

## Features

- **Documentation Access**: Retrieve articles, guides, and tutorials on the MST Chain (smart contracts, accounts, gas, networks, EVM details, etc.).
- **Search & Retrieval**: Easily search keywords across all documentation files or read specific articles.
- **MCP Integration**: Fully compatible with AI assistants and IDEs (Cursor, Claude Desktop, Windsurf).

---

## Quick Setup (No Installation Required)

Since this server is hosted in the cloud, you can connect it directly to your AI assistant without setting up Python or running containers locally.

### Claude Desktop Configuration
Add the following to your configuration file (located at `%APPDATA%\Claude\claude_desktop_config.json` on Windows or `~/Library/Application Support/Claude/claude_desktop_config.json` on macOS):

```json
{
  "mcpServers": {
    "mst-mcp": {
      "command": "npx",
      "args": [
        "-y",
        "mcp-proxy",
        "https://glama.ai/mcp/gateway/vipulsutar11/mst-mcp"
      ]
    }
  }
}
```

### Cursor Configuration
1. Go to **Cursor Settings** > **Features** > **MCP**.
2. Click **+ Add New MCP Server**.
3. Configure the following:
   - **Name**: `mst-mcp`
   - **Type**: `SSE`
   - **URL**: `https://glama.ai/mcp/gateway/vipulsutar11/mst-mcp`

---

## Local Setup & Development

If you want to run the server locally or build/deploy it yourself:

### Prerequisites
- Python 3.10 or higher

### 1. Clone the repository
```bash
git clone https://github.com/vipulsutar11/mst-mcp.git
cd mst-mcp
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the Server
To run the server locally in STDIO mode:
```bash
python server.py
```

### 4. Configure Local AI Client (Claude Desktop)
Add the local server configuration:
```json
{
  "mcpServers": {
    "mst-mcp-local": {
      "command": "python",
      "args": ["/absolute/path/to/server.py"]
    }
  }
}
```

---

## Deploying & Hosting

This project is configured for cloud deployment:
* **Glama**: Configured using `glama.json` and `Dockerfile`. It can be deployed in a sandbox container.
* **Smithery**: Configured using `smithery.yaml`. Can be installed easily by anyone using:
  ```bash
  npx -y @smithery/cli install @vipulsutar11/mst-mcp
  ```

