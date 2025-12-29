#!/usr/bin/env bash
set -euo pipefail

# Run npm commands in a Docker container to avoid local Node.js installation
# Usage: ./scripts/node-docker.sh <npm command>
# Example: ./scripts/node-docker.sh install mermaid-cli
# Example: ./scripts/node-docker.sh run lint-diagrams

if [ $# -eq 0 ]; then
  echo "Usage: $0 <npm command>"
  echo "Example: $0 install mermaid-cli"
  echo "Example: $0 run lint-diagrams"
  exit 1
fi

# Mount the current workspace into the container
WORKSPACE_DIR="$(pwd)"
CONTAINER_WORKDIR="/workspace"

# Run npm in node:latest container
docker run --rm -it \
  -v "${WORKSPACE_DIR}:${CONTAINER_WORKDIR}" \
  -w "${CONTAINER_WORKDIR}" \
  node:latest \
  npm "$@"