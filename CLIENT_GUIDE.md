# MST-MCP Client Installation Guide

This guide is for end-users who want to connect to the **MST-MCP** server to access MST Chain documentation tools. **You do not need to download or clone the repository code.** You only need Docker installed and running on your machine.

---

## Prerequisites
* Install **Docker Desktop** on your machine: [Download Docker Desktop](https://www.docker.com/products/docker-desktop/).
* Make sure Docker Desktop is open and running.

---

## 1. Claude Desktop Setup
To use this server inside your Claude Desktop application:

1. Press `Windows Key + R`, type `%APPDATA%\Claude`, and press **Enter** (on Windows) or open `~/Library/Application Support/Claude` (on macOS).
2. Open `claude_desktop_config.json` in a text editor (like Notepad or VS Code).
3. Paste the following configuration under the `"mcpServers"` object:

```json
{
  "mcpServers": {
    "mst-mcp": {
      "command": "docker",
      "args": [
        "run",
        "-i",
        "--rm",
        "vipulsutar/mst-mcp:1.0.0"
      ]
    }
  }
}
```

4. Save the file and restart **Claude Desktop**. You will see the tools icon (plug/hammer) ready in the message box.

---

## 2. Cursor Setup
To use this server inside the Cursor editor:

1. Go to **Cursor Settings** > **Features** > **MCP**.
2. Click **+ Add New MCP Server**.
3. Configure the settings as follows:
   * **Name**: `mst-mcp`
   * **Type**: `command`
   * **Command**: `docker run -i --rm vipulsutar/mst-mcp:1.0.0`
4. Click **Save**. The status should change to green indicating a successful connection.

---

## 3. Claude Code CLI Setup
To use this server inside your Claude Code terminal assistant:

Simply run the following command in your terminal:
```bash
claude mcp add io.github.vipulsutar11/mst-mcp
```
*(This will automatically configure and link the server using the official MCP Registry metadata).*
