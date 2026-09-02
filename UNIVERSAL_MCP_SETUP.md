# Universal MCP Configuration for DSE Analyst

This document shows how to configure the DSE Analysis MCP server across all AI tools and IDEs.

## Server Details

- **URL:** `http://127.0.0.1:7000`
- **Server Name:** `dse-analysis`
- **Tools:** 16 available (DSE data + technical analysis)

## Configuration for Each Tool

### 1. Claude Desktop / Claude Code

**File:** `~/.claude/mcp.json` or `~/.claude-code-router/mcp_config.json`

```json
{
  "mcpServers": {
    "dse-analysis": {
      "url": "http://127.0.0.1:7000"
    }
  }
}
```

**Steps:**
1. Create the file if it doesn't exist
2. Add the configuration above
3. Restart Claude

### 2. Antigravity IDE

**File:** `~/.antigravity/mcp_config.json` (global) OR `.antigravity.json` in project root

**Global Config:**
```json
{
  "mcpServers": {
    "dse-analysis": {
      "url": "http://127.0.0.1:7000"
    }
  }
}
```

**Project Config:**
```json
{
  "mcpServers": {
    "dse-analysis": {
      "url": "http://127.0.0.1:7000"
    }
  }
}
```

**Location:**
- Global: `~/.antigravity/mcp_config.json`
- Project: `.antigravity.json` or `.antigravity/settings.json`

### 3. Cursor IDE

**File:** `~/.cursor/mcp_config.json` or `~/.cursor_settings/mcp_config.json`

```json
{
  "mcpServers": {
    "dse-analysis": {
      "url": "http://127.0.0.1:7000"
    }
  }
}
```

**Steps:**
1. Create `~/.cursor/` if it doesn't exist
2. Add configuration
3. Restart Cursor

### 4. Windsurf IDE

**File:** `~/.windsurf/mcp_config.json`

```json
{
  "mcpServers": {
    "dse-analysis": {
      "url": "http://127.0.0.1:7000"
    }
  }
}
```

### 5. Zed Editor

**File:** `~/.config/zed/settings.json`

```json
{
  "mcp_servers": {
    "dse-analysis": {
      "url": "http://127.0.0.1:7000"
    }
  }
}
```

Add to existing settings (merge with other settings).

### 6. OpenCode

**File:** `~/.config/opencode/opencode.jsonc`

Add to existing MCP configuration:
```jsonc
{
  "mcp": {
    "dse-analysis": {
      "url": "http://127.0.0.1:7000",
      "enabled": true,
      "type": "http"
    }
  }
}
```

**Steps:**
1. Edit `~/.config/opencode/opencode.jsonc`
2. Add the dse-analysis entry to the "mcp" section
3. Restart OpenCode

### 7. Kilo / Kiro CLI

**File:** `~/.config/kilo/kilo.jsonc`

Add to existing configuration:
```jsonc
{
  "mcp": {
    "dse-analysis": {
      "url": "http://127.0.0.1:7000",
      "enabled": true,
      "type": "http"
    }
  }
}
```

**Steps:**
1. Edit `~/.config/kilo/kilo.jsonc`
2. Add the dse-analysis entry (or create mcp section if doesn't exist)
3. Restart Kilo/Kiro

### 8. Command Line / API Clients

**Environment Variable:**
```bash
export DSE_MCP_URL="http://127.0.0.1:7000"
```

**Python:**
```python
import requests

server_url = "http://127.0.0.1:7000"
response = requests.post(
    f"{server_url}/tool/get_live_price",
    json={"symbol": "BRACBANK"}
)
```

**JavaScript:**
```javascript
const serverUrl = "http://127.0.0.1:7000";
const response = await fetch(`${serverUrl}/tool/full_analysis`, {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ symbol: "GRAMEENPHONE", days: 365 })
});
```

**curl:**
```bash
curl -X POST "http://127.0.0.1:7000/tool/get_market_summary" \
  -H "Content-Type: application/json" \
  -d '{}'
```

## Automated Setup Script

Create `setup_mcp_all.sh`:

```bash
#!/bin/bash

# DSE Analyst MCP Configuration for All AI Tools

MCP_CONFIG='{
  "mcpServers": {
    "dse-analysis": {
      "url": "http://127.0.0.1:7000"
    }
  }
}'

echo "Setting up MCP for all AI tools..."

# Claude
mkdir -p ~/.claude
echo "$MCP_CONFIG" > ~/.claude/mcp.json
echo "✓ Claude Desktop configured"

# Antigravity
mkdir -p ~/.antigravity
echo "$MCP_CONFIG" > ~/.antigravity/mcp_config.json
echo "✓ Antigravity configured"

# Cursor
mkdir -p ~/.cursor
echo "$MCP_CONFIG" > ~/.cursor/mcp_config.json
echo "✓ Cursor configured"

# Windsurf
mkdir -p ~/.windsurf
echo "$MCP_CONFIG" > ~/.windsurf/mcp_config.json
echo "✓ Windsurf configured"

# Zed (merge with existing settings)
mkdir -p ~/.config/zed
if [ -f ~/.config/zed/settings.json ]; then
  echo "⚠ Zed settings exist, manual merge needed"
  echo "Add to ~/.config/zed/settings.json:"
  echo '  "mcp_servers": {
    "dse-analysis": {
      "url": "http://127.0.0.1:7000"
    }
  }'
else
  echo '{
  "mcp_servers": {
    "dse-analysis": {
      "url": "http://127.0.0.1:7000"
    }
  }
}' > ~/.config/zed/settings.json
  echo "✓ Zed configured"
fi

echo ""
echo "✅ MCP setup complete!"
echo ""
echo "Ensure the HTTP server is running:"
echo "  cd /home/sabit/dse/dse-analyst-mcp"
echo "  .venv/bin/python3 server_http.py --transport http --host 127.0.0.1 --port 7000"
```

**Run:**
```bash
bash setup_mcp_all.sh
```

## Server Management

### Start Server

```bash
cd /home/sabit/dse/dse-analyst-mcp

# Using UV
uv run python3 server_http.py --transport http --host 127.0.0.1 --port 7000

# Or directly
.venv/bin/python3 server_http.py --transport http --host 127.0.0.1 --port 7000

# Background
nohup .venv/bin/python3 server_http.py --transport http --host 127.0.0.1 --port 7000 > server.log 2>&1 &
```

### Check Server Status

```bash
ps aux | grep server_http
curl http://127.0.0.1:7000
```

### Stop Server

```bash
pkill -f "server_http.py"
```

## Configuration by Tool

### Tool-Specific Notes

**Claude Desktop:**
- Config in: `~/.claude/mcp.json`
- Restart required: Yes
- Scope: Global (all projects)

**Antigravity:**
- Global: `~/.antigravity/mcp_config.json`
- Project: `.antigravity.json` in project root
- Scope: Can be global or project-specific

**Cursor:**
- Config in: `~/.cursor/mcp_config.json`
- Restart required: Yes
- Scope: Global

**Windsurf:**
- Config in: `~/.windsurf/mcp_config.json`
- Restart required: Yes
- Scope: Global

**Zed:**
- Config in: `~/.config/zed/settings.json`
- Merge with existing: Yes (it's a JSON merge)
- Scope: Global

## Verification

After configuration, verify in each tool:

**Claude:**
Open Claude and check for MCP server in model selector

**Antigravity:**
Open Antigravity, should auto-detect config

**Cursor:**
Check MCP settings in extensions

**Windsurf:**
Check MCP extension

**Zed:**
`zed --version` and check MCP settings

## Testing

### Quick Test in Each Tool

**Claude:**
```
What's the live price of BRACBANK?
@dse-analysis get_live_price BRACBANK
```

**Antigravity:**
```
@dse-analysis get_live_price BRACBANK
```

**Cursor/Windsurf/Zed:**
```
Use assistant with @dse-analysis prefix for tools
```

### Command Line Test

```bash
# Verify server is running
curl -s http://127.0.0.1:7000 | head -5

# Get market summary
curl -X POST "http://127.0.0.1:7000/tool/get_market_summary" \
  -H "Content-Type: application/json" \
  -d '{}'
```

## Troubleshooting

**Server not connecting:**
1. Check server is running: `ps aux | grep server_http`
2. Check port: `netstat -tuln | grep 7000`
3. Restart tool after config change

**Tool doesn't recognize MCP:**
1. Verify config file in correct location
2. Check JSON syntax (use `jq` to validate)
3. Restart tool
4. Check tool logs

**Port already in use:**
```bash
lsof -i :7000
kill -9 <PID>
```

**MCP tools not showing:**
1. Ensure server is running
2. Wait 2-3 seconds after starting server
3. Refresh tool (F5 or restart)

## Summary

All tools now configured to use: `http://127.0.0.1:7000`

| Tool | Config Location | Status |
|------|-----------------|--------|
| Claude Desktop | `~/.claude/mcp.json` | ✅ |
| Antigravity | `~/.antigravity/mcp_config.json` | ✅ |
| Cursor | `~/.cursor/mcp_config.json` | ✅ |
| Windsurf | `~/.windsurf/mcp_config.json` | ✅ |
| Zed | `~/.config/zed/settings.json` | ✅ |
| OpenCode | `~/.config/opencode/opencode.jsonc` | ✅ |
| Kilo/Kiro | `~/.config/kilo/kilo.jsonc` | ✅ |

**Next:** Run the setup script or manually create config files, then start the server!
