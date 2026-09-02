# MCP Quick Reference - All AI Tools

## Server Info

```
URL:    http://127.0.0.1:7000
Name:   dse-analysis
Tools:  16 (DSE data + technical analysis)
```

## Configuration Files

| Tool | File | Status |
|------|------|--------|
| Claude | `~/.claude/mcp.json` | ✅ |
| Antigravity | `~/.antigravity/mcp_config.json` | ✅ |
| Cursor | `~/.cursor/mcp_config.json` | ✅ |
| Windsurf | `~/.windsurf/mcp_config.json` | ✅ |
| Zed | `~/.config/zed/settings.json` | ✅ |
| OpenCode | `~/.config/opencode/opencode.jsonc` | ✅ |
| Kilo/Kiro | `~/.config/kilo/kilo.jsonc` | ✅ |

## Quick Commands

**Start Server:**
```bash
cd /home/sabit/dse/dse-analyst-mcp
.venv/bin/python3 server_http.py --transport http --host 127.0.0.1 --port 7000
```

**Check Status:**
```bash
ps aux | grep server_http
curl http://127.0.0.1:7000
```

**Stop Server:**
```bash
pkill -f "server_http.py"
```

## Using in Each Tool

### Claude
```
@dse-analysis get_live_price BRACBANK
```

### Antigravity
```
@dse-analysis full_analysis GRAMEENPHONE 365
```

### Cursor / Windsurf
```
@dse-analysis analyze_momentum ISLAMIBANK
```

### Zed
```
@dse-analysis scan_top_stocks momentum 20
```

## Available Tools

**Market Data:**
- `get_live_price` - Real-time price
- `get_historical_data` - OHLCV candles
- `get_market_summary` - Index values
- `get_top_gainers` - Top gainers today
- `get_top_losers` - Top losers today
- `get_all_live_prices` - All DSE stocks
- `get_company_info` - Fundamentals

**Technical Analysis:**
- `analyze_trend` - Moving averages
- `analyze_momentum` - RSI, MACD
- `analyze_volatility` - Bollinger Bands
- `analyze_volume` - OBV, VWAP
- `get_fibonacci_levels` - Fib retracements
- `get_ichimoku_cloud` - Ichimoku
- `get_pivot_points` - S/R levels
- `full_analysis` - All indicators
- `scan_top_stocks` - Stock scanner

## File Locations

```
Global Config:
  ~/.claude/mcp.json
  ~/.antigravity/mcp_config.json
  ~/.cursor/mcp_config.json
  ~/.windsurf/mcp_config.json
  ~/.config/zed/settings.json

Project Config:
  /home/sabit/dse/dse-analyst-mcp/.antigravity.json
  /home/sabit/dse/dse-analyst-mcp/.antigravity/settings.json

Server Code:
  /home/sabit/dse/dse-analyst-mcp/server_http.py
```

## Troubleshooting

**Server not running?**
```bash
ps aux | grep server_http
```

**Port in use?**
```bash
lsof -i :7000
kill -9 <PID>
```

**Tool not connecting?**
- Restart the tool
- Check JSON syntax in config
- Verify server is running

## Documentation

- `UNIVERSAL_MCP_SETUP.md` - Full setup guide
- `CLIENT_CONFIG.md` - Detailed examples
- `UV_MIGRATION.md` - Package manager info
- `DEPLOYMENT.md` - Production setup

## Example Queries

**Get live price:**
```
@dse-analysis get_live_price BRACBANK
```

**Full analysis:**
```
@dse-analysis full_analysis GRAMEENPHONE 365
```

**Scan momentum stocks:**
```
@dse-analysis scan_top_stocks momentum 20
```

**Get market summary:**
```
@dse-analysis get_market_summary
```

**Top gainers:**
```
@dse-analysis get_top_gainers 10
```

## Server Details

- **Address:** 127.0.0.1
- **Port:** 7000
- **Protocol:** HTTP (FastMCP)
- **Python:** 3.12.3
- **Status:** Running

## Setup Summary

✅ Claude - configured  
✅ Antigravity - configured  
✅ Cursor - configured  
✅ Windsurf - configured  
✅ Zed - configured  

**All tools ready to use!**
