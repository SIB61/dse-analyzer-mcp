# DSE Analyst MCP — Antigravity Project Setup

## Quick Start

1. **Ensure HTTP server is running:**
   ```bash
   cd /home/sabit/dse/dse-analyst-mcp
   .venv/bin/python3 server_http.py --transport http --host 127.0.0.1 --port 7000
   ```

2. **Open this project in Antigravity:**
   ```bash
   antigravity /home/sabit/dse/dse-analyst-mcp
   ```

3. **Antigravity automatically loads the MCP config** from:
   - `.antigravity.json` (root) or
   - `.antigravity/settings.json` (workspace)

4. **Start using DSE tools in the editor!**

## Project Configuration Files

| File | Purpose |
|------|---------|
| `.antigravity.json` | Root MCP config (auto-detected by Antigravity) |
| `.antigravity/settings.json` | Workspace settings (same config) |
| `.antigravity/README.md` | Setup guide in project |

## MCP Server Details

- **Name:** `dse-analysis`
- **URL:** `http://127.0.0.1:7000`
- **Transport:** HTTP (FastMCP)
- **Scope:** Project-local (not global)

## Using MCP in Antigravity

Once the project is open in Antigravity, use the DSE tools:

### Example Queries:

```
Get live price:
@dse-analysis get_live_price BRACBANK

Full technical analysis:
@dse-analysis full_analysis GRAMEENPHONE

Scan momentum stocks:
@dse-analysis scan_top_stocks momentum 20

Get market summary:
@dse-analysis get_market_summary
```

## Server Management

### Start Server
```bash
cd /home/sabit/dse/dse-analyst-mcp
.venv/bin/python3 server_http.py --transport http --host 127.0.0.1 --port 7000 &
```

### Check Status
```bash
ps aux | grep server_http
curl http://127.0.0.1:7000
```

### View Logs
```bash
tail -f /tmp/dse_server.log
```

### Stop Server
```bash
pkill -f "server_http.py"
```

## Project Structure

```
dse-analyst-mcp/
├── .antigravity.json              ← MCP config (root)
├── .antigravity/                  ← Antigravity workspace folder
│   ├── settings.json              ← MCP config (workspace)
│   └── README.md                  ← Setup guide
├── server_http.py                 ← HTTP MCP server
├── server.py                       ← Original stdio server
├── dse_data.py                    ← DSE data layer
├── technical_analysis.py          ← TA indicators
├── requirements.txt               ← Dependencies
├── DEPLOYMENT.md                  ← Deployment guide
├── CLIENT_CONFIG.md               ← Client examples
└── [other documentation files]
```

## Available Tools (16 total)

### DSE Data (7)
- `get_live_price(symbol)` — Real-time price
- `get_historical_data(symbol, days)` — OHLCV candles
- `get_market_summary()` — Index values
- `get_top_gainers(n)` — Top gaining stocks
- `get_top_losers(n)` — Top losing stocks
- `get_all_live_prices()` — All DSE stocks
- `get_company_info(symbol)` — Company fundamentals

### Technical Analysis (9)
- `analyze_trend(symbol, days)` — Moving averages
- `analyze_momentum(symbol, days)` — RSI, MACD, Stochastic
- `analyze_volatility(symbol, days)` — Bollinger Bands, ATR
- `analyze_volume(symbol, days)` — OBV, VWAP
- `get_fibonacci_levels(symbol, days, lookback)` — Fib retracements
- `get_ichimoku_cloud(symbol, days)` — Ichimoku indicator
- `get_pivot_points(symbol, days)` — Support/resistance
- `full_analysis(symbol, days)` — All indicators + verdict
- `scan_top_stocks(style, top_n, shariah_only)` — Stock scanner

## Troubleshooting

**"MCP server not found" in Antigravity:**
1. Check server is running: `ps aux | grep server_http`
2. Check port 7000: `netstat -tuln | grep 7000`
3. Test connection: `curl http://127.0.0.1:7000`
4. Restart Antigravity and re-open the project

**"Connection refused":**
1. Start the server: `cd /home/sabit/dse/dse-analyst-mcp && .venv/bin/python3 server_http.py --transport http --host 127.0.0.1 --port 7000`
2. Wait 2 seconds for startup
3. Reload Antigravity

**Port already in use:**
1. Kill existing process: `pkill -f "server_http.py"`
2. Start server on different port: `...server_http.py ... --port 7001`
3. Update `.antigravity.json` with new port

## Project-Only Configuration

This MCP configuration is **local to this project**:
- Does NOT affect global Antigravity settings
- Only loads when opening this specific project
- Other projects use their own configs

## Key Files Reference

- **Server Code:** `server_http.py` (711 lines)
- **Main Docs:** `DEPLOYMENT.md`, `CLIENT_CONFIG.md`, `GUIDE.md`
- **Technical Code:** `dse_data.py`, `technical_analysis.py`

## Next Steps

1. ✅ HTTP server is running on port 7000
2. ✅ Project MCP config created (.antigravity.json)
3. 🔜 Open this project in Antigravity
4. 🔜 Start querying DSE data!

---

**Status:** Ready for use. Server running on `http://127.0.0.1:7000`
