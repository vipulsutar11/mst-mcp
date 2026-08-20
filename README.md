# MST-MCP Server

An official Model Context Protocol (MCP) server for the **MST Chain** ecosystem. This server provides tools for LLMs (like Claude) to search, list, and retrieve MST developer documentation (APIs, wallets, transactions, authentication, etc.).

## 🚀 Deployed Endpoint
* **Base URL (SSE Transport):** `https://mst-mcp.onrender.com/sse`
* **Favicon / Branding:** `https://mst-mcp.onrender.com/favicon.png`

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

### Deploying on Render
1. Create a new **Web Service** on Render.
2. Connect your Git repository.
3. Choose the **Docker** runtime (it automatically uses the workspace [`Dockerfile`](./Dockerfile)).
4. Configure environment variables (like `PORT`).
5. Render will automatically build the container and deploy the secure SSE endpoint.
