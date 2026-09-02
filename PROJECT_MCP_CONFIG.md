# Project-Level MCP Configuration

This project has MCP (Model Context Protocol) configured **at the project level only** — not globally. This means the DSE Analyst MCP server is available only when working within this project directory.

## Configuration Structure

```
/home/sabit/dse/dse-analyst-mcp/
├── .claude/
│   └── mcp.json                    ← Claude project config
├── .cursor/
│   └── mcp_config.json             ← Cursor project config
├── .windsurf/
│   └── mcp_config.json             ← Windsurf project config
├── .zed/
│   └── settings.json               ← Zed project config
├── .opencode/
│   └── opencode.jsonc              ← OpenCode project config
├── .kilo/
│   └── kilo.jsonc                  ← Kilo/Kiro project config
├── .antigravity.json               ← Antigravity project config (root)
├── .antigravity/
│   └── settings.json               ← Antigravity project config (workspace)
└── [project files]
```

## How to Use

### For Each Tool

1. **Open this project directory** in your AI tool:
   ```bash
   # Claude
   claude /home/sabit/dse/dse-analyst-mcp
   
   # Antigravity
   antigravity /home/sabit/dse/dse-analyst-mcp
   
   # Cursor
   cursor /home/sabit/dse/dse-analyst-mcp
   
   # Windsurf
   windsurf /home/sabit/dse/dse-analyst-mcp
   
   # Zed
   zed /home/sabit/dse/dse-analyst-mcp
   
   # OpenCode
   opencode /home/sabit/dse/dse-analyst-mcp
   
   # Kiro CLI
   kiro start /home/sabit/dse/dse-analyst-mcp
   ```

2. **The tool will auto-detect** the MCP configuration for this project

3. **Start using DSE tools:**
   ```
   @dse-analysis get_live_price BRACBANK
   ```

## MCP Server Details

- **URL:** `http://127.0.0.1:7000`
- **Name:** `dse-analysis`
- **Scope:** Project-only (not global)
- **Tools:** 16 available

## Available Tools

See main documentation: [GUIDE.md](../GUIDE.md) or [CLIENT_CONFIG.md](../CLIENT_CONFIG.md)

## Server Management

```bash
# Check if server is running
ps aux | grep server_http

# Start server
cd /home/sabit/dse/dse-analyst-mcp
.venv/bin/python3 server_http.py --transport http --host 127.0.0.1 --port 7000

# Stop server
pkill -f "server_http.py"
```

## Key Differences

| Aspect | Global Config | Project Config |
|--------|---------------|----------------|
| Location | `~/.tool/config.json` | `.tool/config.json` (project dir) |
| Scope | All projects | This project only |
| Effect | Tool-wide MCP | Project-specific MCP |
| Use | Default tools | Project-specialized tools |

## This Project

This project uses **project-level configuration** so:
- DSE Analyst MCP is **only available** when working in this directory
- Other projects are **not affected**
- Settings are **version-controllable** (can be committed to git)
- Perfect for **team collaboration** with specific tools

## How Tools Detect Project Config

Each tool looks for its configuration files in the project directory when you open it:

- **Claude**: Looks for `.claude/mcp.json`
- **Antigravity**: Looks for `.antigravity.json` or `.antigravity/settings.json`
- **Cursor**: Looks for `.cursor/mcp_config.json`
- **Windsurf**: Looks for `.windsurf/mcp_config.json`
- **Zed**: Looks for `.zed/settings.json`
- **OpenCode**: Looks for `.opencode/opencode.jsonc`
- **Kilo/Kiro**: Looks for `.kilo/kilo.jsonc`

## Testing

To verify MCP is working in this project:

1. Open this directory in your tool
2. Try a DSE query: `@dse-analysis get_market_summary`
3. If successful, you'll see market data

## Documentation

- [UNIVERSAL_MCP_SETUP.md](UNIVERSAL_MCP_SETUP.md) — Setup details
- [MCP_QUICK_REFERENCE.md](MCP_QUICK_REFERENCE.md) — Quick commands
- [CLIENT_CONFIG.md](CLIENT_CONFIG.md) — Detailed examples

## Notes

- Global settings remain unchanged — other projects are unaffected
- Server must be running (`http://127.0.0.1:7000`)
- Configuration files can be committed to git
- Perfect for team projects that need consistent tooling

---

**Status:** ✅ Project-level MCP configured for all 7 AI tools
