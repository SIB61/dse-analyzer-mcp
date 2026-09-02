#!/bin/bash

# DSE Analyst MCP Configuration - Universal Setup
# Sets up MCP for Claude, Antigravity, Cursor, Windsurf, Zed

set -e

echo "╔════════════════════════════════════════════════════════════╗"
echo "║  DSE Analyst MCP - Universal Setup for All AI Tools       ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# Configuration
MCP_CONFIG='{
  "mcpServers": {
    "dse-analysis": {
      "url": "http://127.0.0.1:7000"
    }
  }
}'

MCP_CONFIG_ZED='{
  "mcp_servers": {
    "dse-analysis": {
      "url": "http://127.0.0.1:7000"
    }
  }
}'

# Counter
count=0

# 1. Claude Desktop
echo "1️⃣  Setting up Claude Desktop..."
mkdir -p ~/.claude
echo "$MCP_CONFIG" > ~/.claude/mcp.json
echo "   ✓ ~/.claude/mcp.json"
((count++))

# 2. Antigravity Global
echo "2️⃣  Setting up Antigravity (global)..."
mkdir -p ~/.antigravity
echo "$MCP_CONFIG" > ~/.antigravity/mcp_config.json
echo "   ✓ ~/.antigravity/mcp_config.json"
((count++))

# 3. Cursor
echo "3️⃣  Setting up Cursor..."
mkdir -p ~/.cursor
echo "$MCP_CONFIG" > ~/.cursor/mcp_config.json
echo "   ✓ ~/.cursor/mcp_config.json"
((count++))

# 4. Windsurf
echo "4️⃣  Setting up Windsurf..."
mkdir -p ~/.windsurf
echo "$MCP_CONFIG" > ~/.windsurf/mcp_config.json
echo "   ✓ ~/.windsurf/mcp_config.json"
((count++))

# 5. Zed
echo "5️⃣  Setting up Zed..."
mkdir -p ~/.config/zed
if [ -f ~/.config/zed/settings.json ]; then
  echo "   ⚠️  Zed settings exist, requires manual merge:"
  echo "   Add to ~/.config/zed/settings.json:"
  echo '   "mcp_servers": {'
  echo '     "dse-analysis": {'
  echo '       "url": "http://127.0.0.1:7000"'
  echo '     }'
  echo '   }'
else
  echo "$MCP_CONFIG_ZED" > ~/.config/zed/settings.json
  echo "   ✓ ~/.config/zed/settings.json"
  ((count++))
fi

echo ""
echo "╔════════════════════════════════════════════════════════════╗"
echo "✅ MCP Setup Complete!"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""
echo "📋 Configured Tools: $count"
echo ""
echo "🚀 Next Steps:"
echo "   1. Start the HTTP server:"
echo "      cd /home/sabit/dse/dse-analyst-mcp"
echo "      .venv/bin/python3 server_http.py --transport http --host 127.0.0.1 --port 7000"
echo ""
echo "   2. Restart your AI tools (Claude, Antigravity, Cursor, Windsurf, Zed)"
echo ""
echo "   3. The MCP server will be available in all tools"
echo ""
echo "✨ Configuration Files Created:"
echo "   • ~/.claude/mcp.json"
echo "   • ~/.antigravity/mcp_config.json"
echo "   • ~/.cursor/mcp_config.json"
echo "   • ~/.windsurf/mcp_config.json"
echo "   • ~/.config/zed/settings.json (if created new)"
echo ""
echo "📌 Server URL: http://127.0.0.1:7000"
echo "📌 Tools Available: 16 (DSE data + technical analysis)"
echo ""
echo "✅ Setup ready!"
