# DSE Analysis MCP Server

A custom [Model Context Protocol](https://modelcontextprotocol.io) server that connects any MCP-compatible AI client to live Dhaka Stock Exchange (DSE) data and a full technical analysis engine. Works with Claude Code, Cursor, Windsurf, Zed, and any other client that supports MCP. Built and tested primarily with Claude.

---

## Project Structure

```
dse-analyst-mcp/
├── server.py               ← MCP server (stdio mode — local clients)
├── server_http.py          ← MCP server (HTTP mode — remote clients) ← NEW
├── dse_data.py             ← DSE data layer (bdshare wrapper)
├── technical_analysis.py   ← Indicators: RSI, MACD, BB, Ichimoku, Fib, etc.
├── requirements.txt        ← Python dependencies
├── .mcp.json               ← Claude Code MCP config (not committed — machine-specific paths)
├── .venv/                  ← Python 3.11/3.12 virtual environment
├── CLAUDE.md               ← Strategy reference (auto-loaded by Claude Code)
├── GUIDE.md                ← User guide: queries, playbooks, indicator reference
├── DEPLOYMENT.md           ← Deployment guide: HTTP server, systemd, Docker, Nginx ← NEW
├── CLIENT_CONFIG.md        ← Client configuration examples (Claude, Cursor, Python, etc.) ← NEW
├── dse-mcp.service         ← Systemd service template ← NEW
├── nginx-dse-mcp.conf      ← Nginx reverse proxy config (SSL/TLS) ← NEW
├── Dockerfile              ← Docker containerization ← NEW
├── docker-compose.yml      ← Docker Compose for easy deployment ← NEW
├── setup.sh                ← Quick setup script ← NEW
└── README.md               ← This file
```

---

## Architecture

### Local (Stdio) Mode
```
You (local MCP client — Claude Code, Cursor, etc.)
       │ command: spawn process
       ▼
  server.py (FastMCP stdio)
  16 registered tools
       │
       ├── DSE Data tools  → dse_data.py  → bdshare → DSE website
       └── TA tools        → technical_analysis.py → pandas/numpy
```

### Remote (HTTP) Mode ← NEW
```
You (any client — Claude, Cursor, Python script, curl, etc.)
       │ http://your-server:8000
       ▼
  server_http.py (FastMCP HTTP)  [on remote server]
  16 registered tools
       │
       ├── DSE Data tools  → dse_data.py  → bdshare → DSE website
       └── TA tools        → technical_analysis.py → pandas/numpy
```

---

## Available Tools (16)

### DSE Data Tools

| Tool | Description |
|------|-------------|
| `get_live_price(symbol)` | Real-time quote — price, change, volume |
| `get_historical_data(symbol, days)` | OHLCV candles for any date range |
| `get_market_summary()` | DSEX, DS30, DSES index values |
| `get_top_gainers(n)` | Top N gaining stocks today |
| `get_top_losers(n)` | Top N losing stocks today |
| `get_all_live_prices()` | Snapshot of all DSE-listed stocks |
| `get_company_info(symbol)` | P/E ratio, EPS, NAV, market cap |

### Technical Analysis Tools

| Tool | Indicators |
|------|------------|
| `analyze_trend(symbol)` | SMA 20/50/200, EMA 9/21/55, Golden/Death Cross |
| `analyze_momentum(symbol)` | RSI (14), MACD (12,26,9), Stochastic, Williams %R, ROC |
| `analyze_volatility(symbol)` | Bollinger Bands (20,2), ATR (14), Historical Volatility |
| `analyze_volume(symbol)` | OBV, VWAP (20), Volume MA, volume ratio |
| `get_fibonacci_levels(symbol)` | Retracements (23.6–78.6%) + extensions (127–261%) |
| `get_ichimoku_cloud(symbol)` | Tenkan, Kijun, Senkou A/B, Chikou, cloud color |
| `get_pivot_points(symbol)` | Classic pivot: Pivot, R1/R2/R3, S1/S2/S3 |
| `full_analysis(symbol)` | All indicators combined + BUY/SELL verdict + confidence % |

### Market Scanner

| Tool | Description |
|------|-------------|
| `scan_top_stocks(style, top_n)` | Scans most active stocks, scores by strategy, returns ranked BUY list with entry/stop/target prices |

**Styles:** `momentum` `swing` `long_term` `breakout` `mean_reversion` `all`

---

## Setup

### Local Development (Stdio Mode)

```bash
# 1. Clone and setup
git clone <this-repo>
cd dse-analyst-mcp
python3.11 -m venv .venv
.venv/bin/pip install -r requirements.txt

# 2. Configure your MCP client to spawn the server locally
# See CLIENT_CONFIG.md for your editor (Claude Code, Cursor, Windsurf, etc.)
```

### Remote Deployment (HTTP Mode) ← NEW

**Quick start** — Run HTTP server locally:
```bash
cd dse-analyst-mcp
.venv/bin/python3 server_http.py --transport http --host 0.0.0.0 --port 8000
```

**Then configure your client to connect to:** `http://your-server-ip:8000`

For production deployment with systemd, Docker, or Nginx + SSL, see [DEPLOYMENT.md](DEPLOYMENT.md).

### Using Docker

```bash
# Build and run with Docker Compose
docker-compose up -d

# Server will be available at http://localhost:8000
```

For full deployment guide, client config examples, and troubleshooting, see [DEPLOYMENT.md](DEPLOYMENT.md) and [CLIENT_CONFIG.md](CLIENT_CONFIG.md).

---

## Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| `mcp` | 1.27.2 | Anthropic MCP Python SDK |
| `bdshare` | 1.2.1 | DSE live + historical data scraper |
| `pandas` | 3.0.3 | DataFrame / OHLCV manipulation |
| `numpy` | 2.4.6 | Numerical computing |
| `ta` | 0.11.0 | Supplemental TA library |
| `uvicorn` | 0.27.0 | ASGI server for HTTP mode |

Runtime: **Python 3.11** (Homebrew). `pandas-ta` not used — all indicators are implemented natively in `technical_analysis.py`.

---

## Troubleshooting

**MCP server not appearing in your client**
→ Claude Code: `Cmd+Shift+P` → "Developer: Reload Window"
→ Cursor / Windsurf: restart the application
→ Verify the `command` path in your client's MCP config points to the correct `python3.11` inside `.venv`

**Empty data / "No historical data found"**
→ Try during DSE market hours: Sun–Thu, 10:00 AM – 2:30 PM BST (UTC+6)
→ Reduce the `days` parameter — some stocks have limited history

**bdshare fetch errors**
→ DSE's website structure occasionally changes; bdshare may need updating: `.venv/bin/pip install --upgrade bdshare`

**ImportError on startup**
→ Run `.venv/bin/python3.11 server.py` manually to see the full traceback

---

## Further Reading

- [GUIDE.md](GUIDE.md) — example queries, trading style playbooks, indicator reference, risk management
- [CLAUDE.md](CLAUDE.md) — world-famous strategies reference (auto-loaded by Claude Code; adapt as a system prompt or context file for other clients)
