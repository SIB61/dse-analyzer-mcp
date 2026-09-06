#!/usr/bin/env bash
set -e

# Determine script directory and project root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

echo "============================================================"
echo "  DSE Analyzer MCP Server — Local Setup (stdio transport)  "
echo "============================================================"
echo "Project Root: ${PROJECT_ROOT}"
echo ""

# Step 1: Check Python 3 installation
echo "[1/4] Checking Python environment..."
if ! command -v python3 &> /dev/null; then
    echo "ERROR: python3 is required but not found in PATH." >&2
    exit 1
fi
PYTHON_VERSION=$(python3 --version 2>&1)
echo "Found ${PYTHON_VERSION}"

# Step 2: Check or install Astral uv
echo ""
echo "[2/4] Checking uv package manager..."
if ! command -v uv &> /dev/null; then
    echo "uv not found. Installing Astral uv package manager..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    export PATH="$HOME/.local/bin:$HOME/.cargo/bin:$PATH"
    if ! command -v uv &> /dev/null; then
        echo "ERROR: uv installation failed or binary not found in PATH." >&2
        exit 1
    fi
fi
UV_VERSION=$(uv --version 2>&1)
echo "Found ${UV_VERSION}"

# Step 3: Sync virtual environment & install dependencies
echo ""
echo "[3/4] Installing project dependencies with uv..."
cd "$PROJECT_ROOT"
uv sync

# Step 4: Verify server modules
echo ""
echo "[4/4] Verifying DSE Analyzer server modules..."
uv run python -c "import server, dse_data, technical_analysis; print('✓ All server modules imported successfully!')"

echo ""
echo "============================================================"
echo "  Setup Complete! DSE Analyzer MCP Server is ready.       "
echo "============================================================"
echo ""
echo "To test the server locally with stdio transport, run:"
echo "  uv run dse-analyst-mcp --transport stdio"
echo ""
echo "Refactored agent MCP configuration files (stdio transport):"
echo "  - Antigravity  : agent-mcp/.agents/mcp_config.json"
echo "  - Command Code : agent-mcp/commandcode.json & agent-mcp/.commandcode/mcp.json"
echo "  - OpenCode     : agent-mcp/opencode.json"
echo "  - Kiro         : agent-mcp/.kiro/settings/mcp.json"
echo "  - Codex        : agent-mcp/.codex/config.toml"
echo ""
