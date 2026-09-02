#!/usr/bin/env bash
set -euo pipefail

IMAGE="ghcr.io/sib61/dse-analyzer-mcp:main"
CONTAINER="dse-analyzer-mcp"
WORKSPACE="$HOME/.dse-analyzer-mcp"

ARCH=$(uname -m)
case "$ARCH" in
  x86_64)  PLATFORM="linux/amd64" ;;
  aarch64|arm64) PLATFORM="linux/arm64" ;;
  *) echo "Unsupported architecture: $ARCH"; exit 1 ;;
esac

echo "==> Pulling $IMAGE ($PLATFORM) ..."
docker pull --platform "$PLATFORM" "$IMAGE"

echo "==> Setting up workspace at $WORKSPACE ..."
mkdir -p "$WORKSPACE"

echo "==> Starting $CONTAINER ..."
docker rm -f "$CONTAINER" >/dev/null 2>&1 || true
docker run -d \
  --name "$CONTAINER" \
  --platform "$PLATFORM" \
  -p 8765:8765 \
  -v "$WORKSPACE":/app/mcp-configs \
  --restart unless-stopped \
  "$IMAGE"

echo "==> Waiting for server to be healthy ..."
for i in $(seq 1 30); do
  if docker exec "$CONTAINER" .venv/bin/python -c "import requests; requests.get('http://localhost:8765')" >/dev/null 2>&1; then
    echo "    Server is up."
    break
  fi
  sleep 1
done

echo ""
echo "Done! Server running at http://localhost:8765"
echo ""
echo "Workspace: $WORKSPACE"
echo ""