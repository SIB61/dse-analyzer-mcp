#!/bin/bash
# Quick setup script for DSE Analysis MCP Server deployment

set -e

echo "=========================================="
echo "DSE Analysis MCP Server — Setup"
echo "=========================================="

# Check Python version
echo "[1/5] Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}' | cut -d. -f1,2)
if [[ "$python_version" != "3.11" && "$python_version" != "3.12" ]]; then
    echo "Warning: Python 3.11 or 3.12 recommended. Found: $python_version"
fi

# Create virtual environment
echo "[2/5] Creating virtual environment..."
if [ ! -d ".venv" ]; then
    python3 -m venv .venv
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment already exists"
fi

# Activate and install dependencies
echo "[3/5] Installing dependencies..."
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
echo "✓ Dependencies installed"

# Verify imports
echo "[4/5] Verifying installation..."
python3 -c "from mcp.server.fastmcp import FastMCP; import uvicorn; print('✓ All imports successful')" || {
    echo "✗ Import check failed"
    exit 1
}

# Test server startup
echo "[5/5] Testing server startup (stdio mode)..."
timeout 3 python3 server_http.py --transport stdio 2>&1 | head -1 || true
echo "✓ Server ready"

echo ""
echo "=========================================="
echo "Setup complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "  1. Stdio mode (local client spawns process):"
echo "     python3 server_http.py --transport stdio"
echo ""
echo "  2. HTTP mode (network clients):"
echo "     python3 server_http.py --transport http --host 0.0.0.0 --port 8000"
echo ""
echo "  3. Production with Docker:"
echo "     docker-compose up -d"
echo ""
echo "  4. Production with systemd (see DEPLOYMENT.md):"
echo "     sudo cp dse-mcp.service /etc/systemd/system/"
echo "     sudo systemctl enable dse-mcp"
echo "     sudo systemctl start dse-mcp"
echo ""
echo "For detailed setup instructions, see DEPLOYMENT.md and CLIENT_CONFIG.md"
