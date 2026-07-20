#!/usr/bin/env bash
#
# start-tunnel.sh — Establish SSH tunnel for remote Godot MCP access.
#
# Usage:
#   ./start-tunnel.sh <user@host> [mcp_port] [runtime_port]
#
# Default ports:
#   MCP HTTP proxy : 14095  →  maps to target:14095
#   Godot runtime  : 9090   →  maps to target:9090  (used by godot-mcp internally)
#
# Requires:
#   - SSH access to the target device
#   - godot-mcp server running on target (started via godot-mcp-service.sh)
#
# Examples:
#   ./start-tunnel.sh alrcatraz@rog-strix.local
#   ./start-tunnel.sh user@workstation.example.com 14095 9090
#

set -euo pipefail

SSH_TARGET="${1:?Usage: $0 <user@host> [mcp_port] [runtime_port]}"
MCP_PORT="${2:-14095}"
RUNTIME_PORT="${3:-9090}"

echo "🔌 Setting up SSH tunnel to ${SSH_TARGET}..."
echo "   MCP HTTP proxy : localhost:${MCP_PORT} → ${SSH_TARGET}:${MCP_PORT}"
echo "   Godot runtime  : localhost:${RUNTIME_PORT} → ${SSH_TARGET}:${RUNTIME_PORT}"

ssh -L "${MCP_PORT}:127.0.0.1:${MCP_PORT}" \
    -L "${RUNTIME_PORT}:127.0.0.1:${RUNTIME_PORT}" \
    -N -o ExitOnForwardFailure=yes \
    "${SSH_TARGET}"

echo "✅ Tunnel closed."
