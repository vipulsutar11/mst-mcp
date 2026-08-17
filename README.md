# MST-MCP Server

An MCP (Model Context Protocol) server designed for the MST Chain ecosystem. This server provides tools and resources to access MST Chain documentation, network information, smart contract deployment guides, wallet balances, and transaction details.

## Features

- **Documentation Access**: Retrieve articles, guides, and tutorials on the MST Chain (smart contracts, accounts, gas, networks, EVM details, etc.).
- **Blockchain Connectivity**: Connect to the MST Chain network via Web3 to query wallet balances, transaction counts, and network status.
- **MCP Integration**: Fully compatible with AI assistants and IDEs (Cursor, Claude Desktop, Windsurf).

## Installation

### Prerequisites

- Python 3.10 or higher
- Node.js & npm (for Smithery deployment/CLI tools)

### 1. Clone the repository
```bash
git clone https://github.com/vipulsutar11/mst-mcp.git
cd mst-mcp
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Setup environment variables
Create a `.env` file in the root directory:
```env
RPC_URL=https://testnetrpc.mstblockchain.com
WALLET_ADDRESS=0xYourWalletAddressHere
```

## Running the Server Locally

To run the server in STDIO mode (default for local integrations):
```bash
python server.py
```

---

## Deploying to Marketplaces (Smithery / Glama)

### Smithery
This project contains a [`smithery.yaml`](smithery.yaml) configuration. To publish it to the Smithery registry:
1. Push the code to a public GitHub repository.
2. Go to [smithery.ai/publish](https://smithery.ai/publish) and connect your repository.
3. Users will then be able to add the server automatically using:
   ```bash
   npx -y smithery@latest mcp add vipulsutar11/mst-mcp
   ```

### Glama
To host this server dynamically on Glama:
1. Connect your GitHub repository to your Glama Workspace.
2. Glama will host your server and generate a secure **SSE (Server-Sent Events)** endpoint URL.
3. Configure the URL in your Claude Desktop or Cursor settings.

---

## Configuration for AI Clients

### Claude Desktop
Add the following to your `%APPDATA%\Claude\claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "mst-mcp": {
      "command": "python",
      "args": ["C:/absolute/path/to/server.py"],
      "env": {
        "RPC_URL": "https://testnetrpc.mstblockchain.com",
        "WALLET_ADDRESS": "0xYourWalletAddressHere"
      }
    }
  }
}
```

### Cursor
1. Go to **Cursor Settings** > **Features** > **MCP**.
2. Click **+ Add New MCP Server**.
3. Name: `mst-mcp`
4. Type: `command`
5. Command: `python C:/absolute/path/to/server.py`
