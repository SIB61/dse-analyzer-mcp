🚀 DSE ANALYSIS MCP SERVER — ANTIGRAVITY CLI CONNECTION
═══════════════════════════════════════════════════════════════

✅ STATUS: SERVER RUNNING

Server Details:
  • URL: http://127.0.0.1:7000
  • Transport: HTTP (FastMCP streamable)
  • Status: Active & Ready
  • PID: (see process below)

Connection Configuration:

  File: ~/.antigravity/mcp_config.json
  
  Content:
  {
    "mcpServers": {
      "dse-analysis": {
        "url": "http://127.0.0.1:7000"
      }
    }
  }

How to Connect Antigravity CLI to the MCP Server:

1. Method 1: Environment Variable
   ──────────────────────────────
   export MCP_SERVER_URL="http://127.0.0.1:7000"
   antigravity <command>

2. Method 2: Command Line Flag
   ────────────────────────────
   antigravity --mcp-server "http://127.0.0.1:7000" <command>

3. Method 3: Via Configuration File
   ──────────────────────────────────
   The config file is already created at:
   ~/.antigravity/mcp_config.json
   
   Restart Antigravity CLI and it should auto-detect

Testing the Connection:

From Command Line:
  antigravity mcp list-tools --server http://127.0.0.1:7000

Or use curl to test directly:
  curl -s http://127.0.0.1:7000 | head

Available DSE Tools (16 total):

DSE Data (7):
  • get_live_price - Real-time stock price
  • get_historical_data - OHLCV candles
  • get_market_summary - Index values
  • get_top_gainers - Top gaining stocks
  • get_top_losers - Top losing stocks
  • get_all_live_prices - All DSE stocks
  • get_company_info - Company fundamentals

Technical Analysis (9):
  • analyze_trend - SMA/EMA, moving averages
  • analyze_momentum - RSI, MACD, Stochastic
  • analyze_volatility - Bollinger Bands, ATR
  • analyze_volume - OBV, VWAP
  • get_fibonacci_levels - Fib retracements
  • get_ichimoku_cloud - Ichimoku indicator
  • get_pivot_points - Support/resistance
  • full_analysis - All indicators combined
  • scan_top_stocks - Stock scanner with scoring

Quick Examples:

Get DSE Market Summary:
  antigravity call get_market_summary --server http://127.0.0.1:7000

Get Live Price (BRACBANK):
  antigravity call get_live_price '{"symbol":"BRACBANK"}' --server http://127.0.0.1:7000

Full Technical Analysis (GRAMEENPHONE):
  antigravity call full_analysis '{"symbol":"GRAMEENPHONE","days":365}' --server http://127.0.0.1:7000

Scan Top Momentum Stocks:
  antigravity call scan_top_stocks '{"trading_style":"momentum","top_n":10}' --server http://127.0.0.1:7000

Server Management:

Check Server Status:
  ps aux | grep server_http
  curl -s http://127.0.0.1:7000

Stop Server:
  pkill -f "server_http.py"

Restart Server:
  cd /home/sabit/dse/dse-analyst-mcp
  .venv/bin/python3 server_http.py --transport http --host 127.0.0.1 --port 7000 &

View Server Logs:
  tail -f /tmp/dse_server.log

Configuration Files:

• MCP Config: ~/.antigravity/mcp_config.json
• Server Code: /home/sabit/dse/dse-analyst-mcp/server_http.py
• Docs: /home/sabit/dse/dse-analyst-mcp/CLIENT_CONFIG.md

Next Steps:

1. Open Antigravity CLI
2. Configure MCP server URL to: http://127.0.0.1:7000
3. Select "dse-analysis" as the active MCP server
4. Start using DSE tools!

Support:

For issues:
  • Check server is running: ps aux | grep server_http
  • Test endpoint: curl http://127.0.0.1:7000
  • Check logs: tail /tmp/dse_server.log
  • Read docs: /home/sabit/dse/dse-analyst-mcp/CLIENT_CONFIG.md
