# DSE Analysis MCP Server — Client Connection Examples

## Claude Code / Claude Desktop

**File:** `~/.claude_desktop_config.json` (or equivalent for your setup)

```json
{
  "mcpServers": {
    "dse-analysis": {
      "url": "http://your-server-ip:8000"
    }
  }
}
```

**Then:** Restart Claude Code and the server should appear in the MCP selector.

---

## Cursor IDE

**File:** `.cursor/mcp_config.json` (in your workspace) or user settings

```json
{
  "mcpServers": {
    "dse-analysis": {
      "url": "http://your-server-ip:8000"
    }
  }
}
```

---

## Windsurf IDE

**File:** `~/.windsurf/mcp_config.json`

```json
{
  "mcpServers": {
    "dse-analysis": {
      "url": "http://your-server-ip:8000"
    }
  }
}
```

---

## Zed IDE

**File:** `~/.config/zed/settings.json`

```json
{
  "mcp_servers": {
    "dse-analysis": {
      "url": "http://your-server-ip:8000"
    }
  }
}
```

---

## Python Client (Custom Integration)

```python
"""Direct HTTP client to DSE Analysis MCP Server."""
import requests
import json

class DSEMCPClient:
    def __init__(self, server_url: str = "http://localhost:8000"):
        self.server_url = server_url
    
    def call_tool(self, tool_name: str, **kwargs) -> dict:
        """Call an MCP tool via HTTP."""
        url = f"{self.server_url}/tool/{tool_name}"
        response = requests.post(url, json=kwargs)
        response.raise_for_status()
        return response.json()
    
    # Convenience methods
    def get_live_price(self, symbol: str) -> dict:
        """Get real-time price for a stock."""
        result = self.call_tool("get_live_price", symbol=symbol)
        return json.loads(result) if isinstance(result, str) else result
    
    def analyze_full(self, symbol: str, days: int = 365) -> dict:
        """Run full technical analysis."""
        result = self.call_tool("full_analysis", symbol=symbol, days=days)
        return json.loads(result) if isinstance(result, str) else result
    
    def scan_stocks(self, style: str = "all", top_n: int = 20) -> dict:
        """Scan and score top DSE stocks."""
        result = self.call_tool("scan_top_stocks", trading_style=style, top_n=top_n)
        return json.loads(result) if isinstance(result, str) else result

# Example usage
if __name__ == "__main__":
    client = DSEMCPClient("http://your-server-ip:8000")
    
    # Get live price
    price = client.get_live_price("BRACBANK")
    print(f"BRACBANK: {price}")
    
    # Full analysis
    analysis = client.analyze_full("GRAMEENPHONE")
    print(f"GRAMEENPHONE Analysis: {analysis}")
    
    # Scan momentum stocks
    scans = client.scan_stocks(style="momentum", top_n=10)
    print(f"Top 10 momentum stocks: {scans['top_buys']}")
```

---

## JavaScript/Node.js Client

```javascript
// client.mjs
const serverUrl = "http://your-server-ip:8000";

async function callTool(toolName, params) {
  const response = await fetch(`${serverUrl}/tool/${toolName}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(params),
  });
  return await response.json();
}

// Example usage
(async () => {
  const price = await callTool("get_live_price", { symbol: "BRACBANK" });
  console.log("BRACBANK:", price);

  const analysis = await callTool("full_analysis", {
    symbol: "GRAMEENPHONE",
    days: 365,
  });
  console.log("Analysis:", analysis);

  const scan = await callTool("scan_top_stocks", {
    trading_style: "momentum",
    top_n: 10,
  });
  console.log("Top buys:", scan.top_buys);
})();
```

---

## curl (Command Line)

```bash
SERVER="http://your-server-ip:8000"

# Get live price
curl -X POST "$SERVER/tool/get_live_price" \
  -H "Content-Type: application/json" \
  -d '{"symbol": "BRACBANK"}'

# Full analysis
curl -X POST "$SERVER/tool/full_analysis" \
  -H "Content-Type: application/json" \
  -d '{"symbol": "GRAMEENPHONE", "days": 365}'

# Scan top momentum stocks
curl -X POST "$SERVER/tool/scan_top_stocks" \
  -H "Content-Type: application/json" \
  -d '{"trading_style": "momentum", "top_n": 20}'
```

---

## Verifying Remote Connection

Before configuring clients, test the server is reachable:

```bash
# From your local machine
curl http://your-server-ip:8000

# Should return MCP server info or docs endpoint
```

If it times out or fails:
1. Check server is running: `sudo systemctl status dse-mcp`
2. Check firewall: `sudo ufw status`
3. Check port is open: `netstat -tuln | grep 8000`
4. Check IP is correct: `hostname -I` (on the server)

---

## Production URLs

| Environment | URL |
|-------------|-----|
| Local dev | `http://127.0.0.1:8000` |
| Local network | `http://192.168.x.x:8000` |
| Remote HTTP | `http://your-domain.com:8000` |
| Remote HTTPS (Nginx) | `https://dse-mcp.example.com` |

**Replace `your-server-ip` or `your-domain.com` with your actual server address.**
