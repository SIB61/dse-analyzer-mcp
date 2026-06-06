# DSE Analysis MCP Server

A custom [Model Context Protocol](https://modelcontextprotocol.io) server that connects Claude directly to live Dhaka Stock Exchange (DSE) data and a full technical analysis engine — running locally via Claude Code.

---

## Project Structure

```
dse-analyst-mcp/
├── server.py               ← MCP server — registers all 16 tools
├── dse_data.py             ← DSE data layer (bdshare wrapper)
├── technical_analysis.py   ← Indicators: RSI, MACD, BB, Ichimoku, Fib, etc.
├── requirements.txt        ← Python dependencies
├── .mcp.json               ← Claude Code MCP config (auto-loaded)
├── .venv/                  ← Python 3.11 virtual environment
├── CLAUDE.md               ← Strategy reference (auto-loaded by Claude Code)
├── GUIDE.md                ← User guide: queries, playbooks, indicator reference
└── README.md               ← This file
```

---

## Architecture

```
You (Claude Code)
       │ natural language question
       ▼
   Claude AI ──── reads .mcp.json ──────────────────────┐
       │                                                 │
       │ picks tool                                      │
       ▼                                                 ▼
  server.py (FastMCP)                            .mcp.json registers
  16 registered tools                            server.py on startup
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

### First time (already done on this machine)

```bash
# 1. Create virtual environment with Python 3.11
python3.11 -m venv .venv

# 2. Install dependencies
.venv/bin/pip install mcp bdshare pandas numpy ta

# 3. Verify
.venv/bin/python3.11 -c "import server; print('OK')"

# 4. Restart Claude Code — it reads .mcp.json automatically
```

### Reinstall on a new machine

```bash
git clone <this repo>
cd dse-analyst-mcp
python3.11 -m venv .venv
.venv/bin/pip install -r requirements.txt
# Restart Claude Code
```

### MCP config (`.mcp.json`)

```json
{
  "mcpServers": {
    "dse-analysis": {
      "command": "/path/to/.venv/bin/python3.11",
      "args": ["/path/to/server.py"]
    }
  }
}
```

Claude Code spawns `server.py` as a subprocess on startup using stdio transport. No internet connection needed beyond what bdshare uses to scrape DSE.

---

## Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| `mcp` | 1.27.2 | Anthropic MCP Python SDK |
| `bdshare` | 1.2.1 | DSE live + historical data scraper |
| `pandas` | 3.0.3 | DataFrame / OHLCV manipulation |
| `numpy` | 2.4.6 | Numerical computing |
| `ta` | 0.11.0 | Supplemental TA library |

Runtime: **Python 3.11** (Homebrew). `pandas-ta` not used — all indicators are implemented natively in `technical_analysis.py`.

---

## Troubleshooting

**MCP server not appearing in Claude Code**
→ Restart: `Cmd+Shift+P` → "Developer: Reload Window"
→ Check `.mcp.json` uses the correct `python3.11` path

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
- [CLAUDE.md](CLAUDE.md) — world-famous strategies reference (auto-loaded by Claude Code)
