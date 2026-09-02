# DSE Analyst MCP Server

An MCP (Model Context Protocol) server that provides **live Dhaka Stock Exchange (DSE) data** and a **comprehensive technical analysis engine**. Connect it to any MCP-compatible AI client (Claude, Cursor, Windsurf, etc.) to analyze DSE stocks with world-famous trading strategies.

## Features

- **Live Market Data** — real-time prices, top gainers/losers, market summary for DSEX, DS30, DSES
- **Technical Analysis** — RSI, MACD, Bollinger Bands, Ichimoku Cloud, Fibonacci, ATR, OBV, Stochastic, and more
- **Stock Scanning** — scan and rank DSE stocks by momentum, swing, breakout, mean reversion, or long-term strategies
- **Trade Planning** — auto-generated entry, stop-loss, target prices, and risk/reward ratios
- **Candlestick Pattern Detection** — engulfing pattern scanner with volume confirmation
- **Shariah Filtering** — built-in list of 280+ Shariah-compliant DSE stocks
- **Company Fundamentals** — P/E ratio, EPS, NAV, market cap

## Installation

### Option 1: Docker (Recommended)

```bash
docker pull ghcr.io/sib61/dse-analyst:main

docker run -d -p 8765:8765 --name dse-analyst ghcr.io/sib61/dse-analyst:main
```

### Option 2: Docker Compose

```bash
git clone https://github.com/SIB61/dse-analyst-mcp.git
cd dse-analyst-mcp
docker compose up -d
```

### Option 3: Local Setup (Python 3.12+)

```bash
git clone https://github.com/SIB61/dse-analyst-mcp.git
cd dse-analyst-mcp

# Install uv (if not installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install dependencies
uv sync

# Run the server
python server.py --transport http --host 0.0.0.0 --port 8765
```

## Usage

### HTTP Mode (remote clients)

```bash
python server.py --transport http --host 0.0.0.0 --port 8765
```

The server will be available at `http://localhost:8765`. API docs at `http://localhost:8765/docs`.

### Stdio Mode (local clients)

```bash
python server.py --transport stdio
```

### MCP Client Configuration

Add to your MCP client config (e.g. Claude Desktop):

```json
{
  "mcpServers": {
    "dse-analyst": {
      "url": "http://localhost:8765/mcp"
    }
  }
}
```

### Example Queries

```
Scan DSE for momentum trades
Run full analysis on BRACBANK
What are the top gainers on DSE today?
Get Fibonacci support levels for GRAMEENPHONE
Scan for mean reversion opportunities
Get company info for SQURPHARMA
```

## Available Tools

| Tool | Description |
|------|-------------|
| `get_live_price` | Real-time price for a DSE stock |
| `get_historical_data` | OHLCV candle data |
| `get_market_summary` | DSEX, DS30, DSES index values |
| `get_top_gainers` / `get_top_losers` | Daily movers |
| `get_company_info` | Fundamentals (P/E, EPS, NAV) |
| `analyze_trend` | SMA/EMA, Golden/Death Cross |
| `analyze_momentum` | RSI, MACD, Stochastic, Williams %R |
| `analyze_volatility` | Bollinger Bands, ATR |
| `analyze_volume` | OBV, VWAP, volume analysis |
| `get_fibonacci_levels` | Retracement & extension levels |
| `get_ichimoku_cloud` | Full Ichimoku analysis |
| `get_pivot_points` | Daily support/resistance levels |
| `full_analysis` | All indicators combined |
| `scan_top_stocks` | Rank stocks by strategy |
| `get_engulfing_pattern` | Single stock pattern detection |
| `scan_engulfing_stocks` | Market-wide pattern scan |

## Tech Stack

- Python 3.12, [MCP SDK](https://github.com/modelcontextprotocol/python-sdk), uvicorn, FastAPI
- [bdshare](https://github.com/aborazmohamed/bdshare) — DSE historical data
- [pandas-ta](https://github.com/twopirllc/pandas-ta) — technical indicators
- [uv](https://github.com/astral-sh/uv) — fast Python package manager

## License

MIT
