#!/usr/bin/env node
const fs = require('fs');
const path = require('path');
const os = require('os');

console.log("Starting MST-MCP configuration installer...");

const homeDir = os.homedir();
const isWindows = process.platform === 'win32';
const isMac = process.platform === 'darwin';

// Paths for Claude Desktop Config
let claudeConfigDir = '';
if (isWindows) {
    claudeConfigDir = path.join(process.env.APPDATA || path.join(homeDir, 'AppData', 'Roaming'), 'Claude');
} else if (isMac) {
    claudeConfigDir = path.join(homeDir, 'Library', 'Application Support', 'Claude');
} else {
    claudeConfigDir = path.join(homeDir, '.config', 'Claude');
}
const claudeConfigPath = path.join(claudeConfigDir, 'claude_desktop_config.json');

// Paths for Cursor Config
let cursorConfigDir = '';
if (isWindows) {
    cursorConfigDir = path.join(process.env.APPDATA || path.join(homeDir, 'AppData', 'Roaming'), 'Cursor', 'User');
} else if (isMac) {
    cursorConfigDir = path.join(homeDir, 'Library', 'Application Support', 'Cursor', 'User');
} else {
    cursorConfigDir = path.join(homeDir, '.config', 'Cursor', 'User');
}
const cursorConfigPath = path.join(cursorConfigDir, 'globalStorage', 'storage.json');

// Target Configuration Details (utilizing official stdio-to-sse bridge)
const serverConfig = {
    command: "npx",
    args: [
        "-y",
        "@modelcontextprotocol/mcp-server-sse",
        "https://mst-mcp.onrender.com/sse"
    ],
    env: {}
};


function ensureDir(dirPath) {
    if (!fs.existsSync(dirPath)) {
        fs.mkdirSync(dirPath, { recursive: true });
    }
}

// 1. Install to Claude Desktop
try {
    ensureDir(claudeConfigDir);
    let config = { mcpServers: {} };
    if (fs.existsSync(claudeConfigPath)) {
        try {
            config = JSON.parse(fs.readFileSync(claudeConfigPath, 'utf8'));
        } catch (e) {
            console.warn("Could not parse existing Claude configuration. Overwriting default.");
        }
    }
    if (!config.mcpServers) config.mcpServers = {};
    config.mcpServers["mst-mcp"] = serverConfig;

    fs.writeFileSync(claudeConfigPath, JSON.stringify(config, null, 2), 'utf8');
    console.log(`Successfully added mst-mcp to Claude Desktop config at: ${claudeConfigPath}`);
} catch (err) {
    console.error(`Failed updating Claude Desktop config: ${err.message}`);
}

// 2. Install to Cursor
const cursorGlobalStorageDir = path.join(cursorConfigDir, 'globalStorage');
try {
    if (fs.existsSync(cursorConfigDir)) {
        ensureDir(cursorGlobalStorageDir);
        let config = {};
        if (fs.existsSync(cursorConfigPath)) {
            try {
                config = JSON.parse(fs.readFileSync(cursorConfigPath, 'utf8'));
            } catch (e) {
                console.warn("Could not parse existing Cursor configuration.");
            }
        }
        
        // Locate or initialize mcpServers key in Cursor storage configuration
        let mcpConfig = {};
        if (config["mcp.mcpServers"]) {
            try {
                mcpConfig = typeof config["mcp.mcpServers"] === 'string' 
                    ? JSON.parse(config["mcp.mcpServers"]) 
                    : config["mcp.mcpServers"];
            } catch (e) {
                mcpConfig = {};
            }
        }
        
        mcpConfig["mst-mcp"] = serverConfig;
        config["mcp.mcpServers"] = JSON.stringify(mcpConfig);

        fs.writeFileSync(cursorConfigPath, JSON.stringify(config, null, 2), 'utf8');
        console.log(`Successfully added mst-mcp to Cursor config at: ${cursorConfigPath}`);
    } else {
        console.log("Cursor configuration folder not found. Skipping Cursor installation.");
    }
} catch (err) {
    console.error(`Failed updating Cursor config: ${err.message}`);
}

console.log("\nSetup complete! Please restart Claude Desktop / Cursor to connect to the MST-MCP server.");
