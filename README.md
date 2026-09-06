# DSE Analyzer MCP Server

An MCP (Model Context Protocol) server that provides **live Dhaka Stock Exchange (DSE) data** and a **comprehensive technical analysis engine**. Connect it to any MCP-compatible AI client or agent framework (Antigravity, OpenCode, Codex, Kiro, Claude Desktop, Cursor, Windsurf) to analyze DSE stocks with quantitative trading strategies.

---

## 🌟 Features

- **Live Market Data** — Real-time stock prices, market volume, top gainers/losers, and index summaries (DSEX, DS30, DSES).
- **Technical Analysis Engine** — RSI, MACD (with divergence), Bollinger Bands (with squeeze detection & %B), Ichimoku Cloud, Fibonacci Retracements/Extensions, ATR (14), OBV, VWAP, and Pivot Points.
- **Stock Scanning & Trade Planning** — Rank stocks across 5 strategies (*Momentum*, *Swing*, *Breakout*, *Mean Reversion*, *Long Term*) with auto-generated entry price, stop-loss, profit targets (T1 & T2), and risk/reward ratios.
- **Candlestick Pattern Detection** — Bullish and Bearish Engulfing pattern scanner with volume confirmation and RSI context.
- **Shariah Filtering** — Built-in list of 280+ Shariah-compliant DSE equities verified against official IBSL and DSES indexes.
- **Company Fundamentals** — P/E ratio, EPS, NAV, and market cap.

---

## 🚀 Quick Start: Local Setup (Recommended)

### 1. Run Automated Setup Script

Clone the repository and run the setup script:

```bash
git clone https://github.com/SIB61/dse-analyzer-mcp.git
cd dse-analyzer-mcp

# Run the automated setup script
./agent/setup.sh
```

`setup.sh` will:
1. Check your Python 3 environment.
2. Install the Astral `uv` package manager if not present.
3. Run `uv sync` to set up dependencies (`mcp`, `bdshare`, `pandas`, `pandas-ta`, `fastapi`, `uvicorn`).
4. Verify all server modules.

---

## ⚙️ Local Stdio Integration Guide (Local AI Agents)

For local AI clients that communicate over Standard I/O (Stdio), the server is executed via `uv run dse-analyst-mcp --transport stdio`.

Pre-configured agent files are available in the [`agent/`](./agent) directory:

### 1. Antigravity (`agy`)
* **Workspace Config**: `.mcp.json` / `.agents/mcp_config.json`
* **Agent Persona**: `.agents/agents/DSE-ANALYZER/agent.md`
* **Configuration**:
  ```json
  {
    "mcpServers": {
      "DSE-ANALYZER": {
        "command": "uv",
        "args": ["run", "dse-analyst-mcp", "--transport", "stdio"],
        "trust": true,
        "autoApprove": ["DSE-ANALYZER/*"]
      }
    }
  }
  ```

### 2. OpenCode
* **Configuration**: `agent/opencode.json`
* **Agent Persona**: `agent/.opencode/agents/DSE-ANALYZER.md`
* **Configuration**:
  ```json
  {
    "$schema": "https://opencode.ai/config.json",
    "mcp": {
      "DSE-ANALYZER": {
        "type": "local",
        "command": ["uv", "run", "dse-analyst-mcp", "--transport", "stdio"],
        "autoApprove": true
      }
    }
  }
  ```

### 3. Codex
* **Configuration**: `agent/.codex/config.toml`
* **Agent Persona**: `agent/.codex/agents/DSE-ANALYZER.toml`
* **Configuration**:
  ```toml
  [mcp_servers.DSE-ANALYZER]
  command = "uv"
  args = ["run", "dse-analyst-mcp", "--transport", "stdio"]
  ```

### 4. Kiro
* **Settings**: `agent/.kiro/settings/mcp.json`
* **Agent Persona**: `agent/.kiro/agents/DSE-ANALYZER.json`
* **Configuration**:
  ```json
  {
    "mcpServers": {
      "DSE-ANALYZER": {
        "command": "uv",
        "args": ["run", "dse-analyst-mcp", "--transport", "stdio"],
        "autoApprove": true
      }
    }
  }
  ```

---

## 🌐 Remote HTTP Server & Docker Options

### Option 1: Docker (Pre-built Image)

```bash
docker pull ghcr.io/sib61/dse-analyzer-mcp:main
docker run -d -p 8765:8765 --name dse-analyzer-mcp ghcr.io/sib61/dse-analyzer-mcp:main
```

### Option 2: Docker Compose

```bash
docker compose up -d
```

### Option 3: Manual HTTP Mode

```bash
uv run dse-analyst-mcp --transport http --host 0.0.0.0 --port 8765
```

- Endpoint: `http://localhost:8765/mcp`
- Interactive API Documentation: `http://localhost:8765/docs`

---

## 🛠️ Available MCP Tools

| Tool | Description |
|------|-------------|
| `get_live_price` | Real-time price, volume, high/low, and daily change |
| `get_historical_data` | Normalized OHLCV candle data |
| `get_market_summary` | DSEX, DS30, DSES index values and total market turnover |
| `get_top_gainers` / `get_top_losers` | Top daily movers |
| `get_company_info` | Fundamental metrics (P/E ratio, EPS, NAV) |
| `analyze_trend` | SMA/EMA moving averages, Golden/Death Cross signals |
| `analyze_momentum` | RSI (14), MACD line/histogram/divergence, Stochastic, Williams %R |
| `analyze_volatility` | Bollinger Bands with squeeze detection, ATR (14) stop-loss calculator |
| `analyze_volume` | On-Balance Volume (OBV) with divergence, 20-period VWAP |
| `get_fibonacci_levels` | Swing high/low retracement (23.6%-78.6%) & extension targets |
| `get_ichimoku_cloud` | Tenkan, Kijun, Senkou Span A/B, Chikou Span, cloud signal |
| `get_pivot_points` | Daily Pivot, R1-R3 resistance, S1-S3 support levels |
| `full_analysis` | Complete quantitative report with aggregated BUY/SELL verdict |
| `scan_top_stocks` | Rank stocks by Momentum, Swing, Breakout, Mean Reversion, or Long Term |
| `get_engulfing_pattern` | Detect Bullish/Bearish Engulfing pattern for a single stock |
| `scan_engulfing_stocks` | Market-wide engulfing pattern scanner with volume confirmation |

---

## 💡 Example Prompt Queries

```
"Scan DSE for momentum trades"
"Run full technical analysis on BRACBANK"
"What are the top gainers on DSE today?"
"Get Fibonacci support levels for GRAMEENPHONE"
"Scan for mean reversion opportunities among Shariah stocks"
"Get company fundamentals for SQURPHARMA"
```

---

## 🛠️ Tech Stack

- Python 3.12, [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk), FastAPI, Uvicorn
- [bdshare](https://github.com/aborazmohamed/bdshare) — DSE market data library
- [pandas-ta](https://github.com/twopirllc/pandas-ta) — Technical indicator engine
- [uv](https://github.com/astral-sh/uv) — Fast Python package manager

---

## 📄 License

MIT
