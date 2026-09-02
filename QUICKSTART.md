# DSE MCP Server — Quick Command Reference

## Start the Server

### HTTP Mode (Network Access)
```bash
# Local testing
python3 server_http.py --transport http --host 127.0.0.1 --port 8000

# Production (all interfaces)
python3 server_http.py --transport http --host 0.0.0.0 --port 8000

# Custom port
python3 server_http.py --transport http --host 0.0.0.0 --port 9000
```

### Stdio Mode (Local Clients Only)
```bash
python3 server_http.py --transport stdio
```

### Docker
```bash
# Quick start
docker-compose up -d

# View logs
docker-compose logs -f dse-mcp

# Stop
docker-compose down
```

### Systemd
```bash
# Install
sudo cp dse-mcp.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable dse-mcp

# Start
sudo systemctl start dse-mcp

# Status
sudo systemctl status dse-mcp
sudo journalctl -u dse-mcp -f

# Stop
sudo systemctl stop dse-mcp
```

---

## Test the Server

### curl (Command Line)
```bash
SERVER="http://127.0.0.1:8000"

# List available tools
curl -X POST "$SERVER/invoke/tools" -H "Content-Type: application/json" -d '{}'

# Get market summary
curl -X POST "$SERVER/tool/get_market_summary" -H "Content-Type: application/json" -d '{}'

# Get live price
curl -X POST "$SERVER/tool/get_live_price" -H "Content-Type: application/json" -d '{"symbol":"BRACBANK"}'

# Full analysis
curl -X POST "$SERVER/tool/full_analysis" -H "Content-Type: application/json" -d '{"symbol":"GRAMEENPHONE","days":365}'

# Scan stocks
curl -X POST "$SERVER/tool/scan_top_stocks" -H "Content-Type: application/json" -d '{"trading_style":"momentum","top_n":10}'
```

### Python
```python
import requests
import json

url = "http://127.0.0.1:8000/tool/get_live_price"
response = requests.post(url, json={"symbol": "BRACBANK"})
print(json.dumps(response.json(), indent=2))
```

---

## Firewall

### UFW (Ubuntu)
```bash
# Allow port
sudo ufw allow 8000/tcp

# Check status
sudo ufw status

# Disable
sudo ufw disable
```

### firewalld (CentOS/RHEL)
```bash
# Allow port permanently
sudo firewall-cmd --permanent --add-port=8000/tcp
sudo firewall-cmd --reload

# Check
sudo firewall-cmd --list-all
```

---

## Monitoring

### Check if Server is Running
```bash
# Port is listening
netstat -tuln | grep 8000
lsof -i :8000

# Process check
ps aux | grep server_http
```

### Server Logs
```bash
# Systemd
sudo journalctl -u dse-mcp -f              # Follow logs
sudo journalctl -u dse-mcp -n 100          # Last 100 lines
sudo journalctl -u dse-mcp --since "1 hour ago"

# Docker
docker-compose logs -f dse-mcp
docker logs dse-mcp

# Manual (capture output)
python3 server_http.py --transport http --host 0.0.0.0 --port 8000 2>&1 | tee server.log
```

---

## Troubleshooting

### Port Already in Use
```bash
# Find what's using the port
lsof -i :8000

# Kill the process
kill -9 <PID>

# Use different port
python3 server_http.py --transport http --host 0.0.0.0 --port 8001
```

### Connection Refused
```bash
# Check server is running
sudo systemctl status dse-mcp

# Check firewall
sudo ufw status
netstat -tuln | grep LISTEN

# Check IP binding
hostname -I                    # Find your IP

# Test from server machine
curl http://127.0.0.1:8000

# Test from remote machine
curl http://<server-ip>:8000
```

### Module Import Errors
```bash
# Reinstall dependencies
.venv/bin/pip install -r requirements.txt

# Verify imports
.venv/bin/python3 -c "import mcp, uvicorn; print('OK')"
```

### No Data / "No historical data found"
```bash
# Check if DSE market is open (Sun-Thu, 10 AM - 2:30 PM BST)
# Try a different stock
# Try fewer days
curl -X POST "http://localhost:8000/tool/get_historical_data" \
  -H "Content-Type: application/json" \
  -d '{"symbol":"GRAMEENPHONE","days":30}'
```

---

## Nginx Reverse Proxy

### Test Configuration
```bash
sudo nginx -t
```

### Reload After Config Change
```bash
sudo systemctl reload nginx
```

### View Access Logs
```bash
tail -f /var/log/nginx/dse-mcp-access.log
```

### Generate SSL Certificate (Let's Encrypt)
```bash
sudo apt-get install certbot python3-certbot-nginx
sudo certbot --nginx -d dse-mcp.example.com
```

---

## Deployment Checklist

- [ ] Dependencies installed: `pip install -r requirements.txt`
- [ ] Server tested locally: `python3 server_http.py --transport http`
- [ ] Firewall allows port 8000
- [ ] Clients can connect to `http://server-ip:8000`
- [ ] For production: Systemd or Docker setup complete
- [ ] For HTTPS: Nginx + SSL configured (optional)
- [ ] Monitoring in place: Check logs regularly
- [ ] Backups: Database/logs stored safely

---

## Common Client URLs

| Setup | URL |
|-------|-----|
| Local dev | `http://127.0.0.1:8000` |
| Same network | `http://192.168.1.100:8000` |
| Remote (HTTP) | `http://your-domain.com:8000` |
| Remote (HTTPS) | `https://dse-mcp.example.com` |

---

## See Also

- `DEPLOYMENT.md` — Full deployment guide
- `CLIENT_CONFIG.md` — Client setup examples
- `HTTP_DEPLOYMENT.md` — Implementation summary
- `.venv/bin/python3 server_http.py --help` — Server help text
