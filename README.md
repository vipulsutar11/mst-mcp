# MST-MCP Server

An official Model Context Protocol (MCP) server for the **MST Chain** ecosystem. This server provides tools for LLMs (like Claude) to search, list, and retrieve MST developer documentation (APIs, wallets, transactions, authentication, etc.).

## 🚀 Deployed Endpoint
* **Base URL (SSE Transport):** `https://mst-mcp-xjb5.onrender.com/sse`
* **Favicon / Branding:** `https://mst-mcp-xjb5.onrender.com/favicon.png`

### 💻 How Developers Can Connect (Claude Desktop, Cursor, Antigravity IDE)

Because IDEs require a standard STDIO connection but the server is hosted remotely, developers must use the provided `sse_bridge.py` script to tunnel the connection.

1. Developers clone this repository:
   ```bash
   git clone https://github.com/vipulsutar11/mst-mcp.git
   cd mst-mcp
   pip install aiohttp
   ```
2. They configure their IDE (e.g. `mcp_config.json` or `claude_desktop_config.json`) to use the bridge script:
   ```json
   {
     "mcpServers": {
       "mst-mcp": {
         "command": "python",
         "args": ["/path/to/cloned/mst-mcp/sse_bridge.py"]
       }
     }
   }
   ```
   *Note: This script automatically handles the Bypass Token and SSE connections.*

---

## 🛠 Exposed Tools

All tools are read-only lookup tools with custom annotations:

1. **`list_documents`**
   * **Description:** Lists all available developer documentation files in the server.
   * **Annotations:** `readOnlyHint: true`, `title: "List Documents"`

2. **`read_document`**
   * **Description:** Reads and returns the contents of a specific documentation file (e.g., `SDK.txt`).
   * **Annotations:** `readOnlyHint: true`, `title: "Read Document"`

3. **`search_documents`**
   * **Description:** Searches for a keyword or query across all files and returns matching lines with line numbers.
   * **Annotations:** `readOnlyHint: true`, `title: "Search Documents"`

---

## 💡 Example Prompts to Try in Claude

After connecting this server as a connector, you can ask Claude:

* **Example 1 (Listing docs):** 
  > "Check my mcp is in working and list all documentation files."
* **Example 2 (Searching keywords):** 
  > "Search the developer docs for wallet integration details."
* **Example 3 (Retrieving document content):** 
  > "Read the documentation on transaction structure."

---

## 🏗 Setup & Deployment

### Local Development
To run the server locally:
1. Initialize virtual environment and install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Start the server:
   ```bash
   python server.py
   ```

### Deploying on AWS EC2
We have provided a dedicated deployment guide for AWS EC2. 
Please refer to the [`DEPLOYMENT.md`](./DEPLOYMENT.md) file for comprehensive, step-by-step instructions on setting up your EC2 instance natively or via Docker.
