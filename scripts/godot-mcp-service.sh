#!/usr/bin/env bash
#
# godot-mcp-service.sh — Start godot-mcp server on the target device.
# Run this on the machine where Godot is installed.
#
# Usage:
#   ./godot-mcp-service.sh                   # Start with defaults
#   ./godot-mcp-service.sh /path/to/godot    # Custom Godot path
#
# Starts:
#   1. godot-mcp MCP server (Node.js, stdio mode)
#   2. mcp-proxy HTTP bridge (so the AI assistant can connect via HTTP)
#
# The mcp-proxy listens on port 14095 by default.
#

set -euo pipefail

GODOT_PATH="${1:-$(which godot 2>/dev/null || echo '/usr/local/bin/godot')}"
MCP_DIR="${MCP_DIR:-$HOME/godot-mcp}"
MCP_PROXY_PORT="${MCP_PROXY_PORT:-14095}"

# Check prerequisites
if ! command -v node &>/dev/null; then
    echo "❌ Node.js not found. Install it first."
    exit 1
fi

if [ ! -d "$MCP_DIR" ]; then
    echo "📦 godot-mcp not found at $MCP_DIR. Cloning..."
    git clone https://github.com/tugcantopaloglu/godot-mcp.git "$MCP_DIR"
    cd "$MCP_DIR"
    npm install && npm run build
fi

cd "$MCP_DIR"

# Export environment for godot-mcp
export GODOT_PATH="$GODOT_PATH"
export DEBUG="${DEBUG:-true}"

echo "🚀 Starting godot-mcp server..."
echo "   Godot path : $GODOT_PATH"
echo "   MCP dir    : $MCP_DIR"

# Start godot-mcp in background, pipe to mcp-proxy for HTTP
# Using tmux so it persists across SSH disconnects
SESSION_NAME="godot-mcp"

if tmux has-session -t "$SESSION_NAME" 2>/dev/null; then
    echo "⚠️  Session '$SESSION_NAME' already exists. Restarting..."
    tmux kill-session -t "$SESSION_NAME"
fi

tmux new-session -d -s "$SESSION_NAME" -x 120 -y 30
tmux send-keys -t "$SESSION_NAME" "cd $MCP_DIR && export GODOT_PATH=$GODOT_PATH && npx mcp-proxy --transport streamable-http http://127.0.0.1:${MCP_PROXY_PORT}/mcp -- node build/index.js" Enter

echo "✅ godot-mcp running in tmux session '$SESSION_NAME'"
echo "   MCP endpoint: http://127.0.0.1:${MCP_PROXY_PORT}/mcp"
echo ""
echo "📋 From your AI assistant machine, run:"
echo "   ssh -L ${MCP_PROXY_PORT}:127.0.0.1:${MCP_PROXY_PORT} user@this-machine"
echo ""
echo "   Then configure Hermes:"
echo "   hermes mcp add godot --url http://127.0.0.1:${MCP_PROXY_PORT}/mcp"
