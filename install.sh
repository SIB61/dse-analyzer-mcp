#!/usr/bin/env bash
set -euo pipefail

IMAGE="ghcr.io/sib61/dse-analyzer:main"
CONTAINER="dse-mcp"
VOLUME="dse-analyzer"

echo "==> Pulling $IMAGE ..."
docker pull "$IMAGE"

echo "==> Creating volume $VOLUME (if not exists) ..."
docker volume create "$VOLUME" >/dev/null 2>&1 || true

echo "==> Starting $CONTAINER ..."
docker rm -f "$CONTAINER" >/dev/null 2>&1 || true
docker run -d \
  --name "$CONTAINER" \
  -p 8765:8765 \
  -v "$VOLUME":/app/mcp-configs \
  -v dse-analyzer-opencode:/root/.config/opencode \
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

echo "==> Copying MCP configs into container ..."
docker cp mcp-configs/. "$CONTAINER":/app/mcp-configs/

echo "==> Setting up opencode config ..."
docker exec "$CONTAINER" bash -c 'mkdir -p /root/.config/opencode && cp /app/mcp-configs/opencode.json /root/.config/opencode/opencode.json'

echo ""
echo "Done! Server running at http://localhost:8765"
echo ""
echo "To open opencode inside the container:"
echo "  docker exec -it $CONTAINER opencode"
