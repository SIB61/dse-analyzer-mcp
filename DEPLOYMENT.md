# DSE Analysis MCP Server — HTTP Deployment Guide

## Overview

The server now supports both **HTTP** (for remote/network connections) and **Stdio** (for local clients) transports.

- **HTTP Mode**: Run as a network service; clients connect via URL (`http://server:8000`)
- **Stdio Mode**: Run as a subprocess; clients spawn the process directly (default, for local use)

---

## Quick Start: Run Locally (HTTP)

```bash
cd dse-analyst-mcp
.venv/bin/python3 server_http.py --transport http --host 127.0.0.1 --port 8000
```

Then point your MCP client to: `http://127.0.0.1:8000`

---

## Production Deployment

### Option A: Direct Server (Linux/Mac)

Ideal for small deployments, VPS, or home server.

#### 1. Clone and set up on your server

```bash
git clone <this-repo> dse-analyst-mcp
cd dse-analyst-mcp
python3.11 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

#### 2. Run with systemd (recommended for uptime)

Create a systemd service file: `/etc/systemd/system/dse-mcp.service`

```ini
[Unit]
Description=DSE Analysis MCP Server
After=network.target

[Service]
Type=simple
User=<your-username>
WorkingDirectory=/home/<your-username>/dse-analyst-mcp
ExecStart=/home/<your-username>/dse-analyst-mcp/.venv/bin/python3 server_http.py --transport http --host 0.0.0.0 --port 8000
Restart=on-failure
RestartSec=10

[Install]
WantedBy=multi-user.target
```

**Start the service:**

```bash
sudo systemctl enable dse-mcp          # Auto-start on reboot
sudo systemctl start dse-mcp
sudo systemctl status dse-mcp
```

**View logs:**

```bash
sudo journalctl -u dse-mcp -f          # Follow live logs
```

#### 3. Firewall (if needed)

Allow port 8000 on your server:

```bash
sudo ufw allow 8000/tcp    # UFW
# or
sudo firewall-cmd --permanent --add-port=8000/tcp && sudo firewall-cmd --reload  # firewalld
```

#### 4. Test connectivity

From your local machine:

```bash
curl http://<server-ip>:8000
```

You should see the MCP server's OpenAPI docs or endpoint info.

---

### Option B: Nginx Reverse Proxy (SSL + Security)

For production, use a reverse proxy for SSL/TLS, better security, and cleaner URLs.

#### 1. Install Nginx

```bash
sudo apt-get install nginx
```

#### 2. Create Nginx config: `/etc/nginx/sites-available/dse-mcp`

```nginx
server {
    listen 80;
    server_name dse-mcp.example.com;  # Replace with your domain

    # Redirect HTTP to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name dse-mcp.example.com;

    # SSL certificates (use Let's Encrypt)
    ssl_certificate /etc/letsencrypt/live/dse-mcp.example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/dse-mcp.example.com/privkey.pem;

    # Proxy to MCP server
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_read_timeout 300s;
        proxy_connect_timeout 300s;
    }
}
```

#### 3. Enable and test

```bash
sudo ln -s /etc/nginx/sites-available/dse-mcp /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx

# Use Certbot for free SSL
sudo apt-get install certbot python3-certbot-nginx
sudo certbot --nginx -d dse-mcp.example.com
```

#### 4. Configure clients

Point to: `https://dse-mcp.example.com`

---

### Option C: Docker (Any Cloud / Platform)

For maximum portability.

#### 1. Create `Dockerfile`

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python", "server_http.py", "--transport", "http", "--host", "0.0.0.0", "--port", "8000"]
```

#### 2. Build and run

```bash
docker build -t dse-mcp:latest .
docker run -d -p 8000:8000 --name dse-mcp dse-mcp:latest
```

#### 3. Push to registry (optional)

```bash
docker tag dse-mcp:latest <your-registry>/dse-mcp:latest
docker push <your-registry>/dse-mcp:latest
```

#### 4. Deploy to cloud (AWS ECS, Google Cloud Run, Azure Container Instances, etc.)

Each platform has different steps, but the Docker image works on all.

---

## Client Configuration

### Claude Code (MCP)

Update or create `.mcp.json`:

```json
{
  "mcpServers": {
    "dse-analysis": {
      "url": "http://your-server-ip:8000"
    }
  }
}
```

### Cursor / Windsurf / Zed

Add to your client's MCP settings:

```json
{
  "dse-analysis": {
    "url": "http://your-server-ip:8000"
  }
}
```

### Custom Client (Python)

```python
import requests

server_url = "http://your-server-ip:8000"

# Call a tool via HTTP
response = requests.post(
    f"{server_url}/tool/get_live_price",
    json={"symbol": "BRACBANK"}
)
print(response.json())
```

---

## Monitoring & Maintenance

### Health Check

```bash
curl http://your-server-ip:8000/health
```

### Monitor resource usage (systemd)

```bash
systemctl status dse-mcp
ps aux | grep server_http.py
```

### Restart after crash

The systemd service restarts automatically. Check logs:

```bash
sudo journalctl -u dse-mcp -n 50   # Last 50 lines
```

### Update the code

```bash
cd dse-analyst-mcp
git pull
.venv/bin/pip install --upgrade -r requirements.txt
sudo systemctl restart dse-mcp
```

---

## Security Considerations

1. **Use HTTPS in production** (Nginx + Let's Encrypt is free)
2. **Firewall**: Only expose the port to trusted networks
3. **VPN**: For sensitive use, tunnel over VPN
4. **Rate limiting**: Add Nginx rate limiting or API key middleware if needed
5. **Server hardening**: Keep OS and Python packages up to date

---

## Troubleshooting

**Port already in use:**

```bash
lsof -i :8000
kill -9 <PID>
```

**Server won't start:**

```bash
cd dse-analyst-mcp
.venv/bin/python3 server_http.py --transport http --host 0.0.0.0 --port 8000
# Check output for errors
```

**Clients can't connect:**

- Verify firewall allows port
- Check server IP: `hostname -I`
- Verify service is running: `sudo systemctl status dse-mcp`
- Check logs: `sudo journalctl -u dse-mcp -f`

**Data not loading:**

- DSE only has data during market hours (Sun–Thu, 10 AM – 2:30 PM BST)
- Check bdshare: `.venv/bin/pip install --upgrade bdshare`

---

## Local Development (Stdio Mode)

For local testing without network setup:

```bash
.venv/bin/python3 server.py    # Uses original stdio transport
```

Configure your local MCP client to spawn the process directly.

---

## Summary

| Scenario | Transport | Setup |
|----------|-----------|-------|
| Local development | Stdio | No network config needed |
| Same LAN | HTTP | Direct connection to server:8000 |
| Remote / Production | HTTP + Nginx + SSL | Domain + SSL certificates |
| Cloud deployment | Docker | Deploy to ECS, Cloud Run, etc. |

Choose based on your use case. **Start with HTTP + systemd on a VPS or home server**, then add Nginx for production.
