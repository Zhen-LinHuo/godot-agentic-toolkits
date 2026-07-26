# Setup Guide

Setting up a device for AI-assisted Godot development involves three layers:
the Godot engine, the MCP server, and the Python training environment.

## Prerequisites

- Godot **4.4+** (4.7 recommended), **.NET/C# version** for C# projects
- Node.js >= 18 on the machine running the MCP server
- Python 3.10+ with `uv` for training

## 1. Install Godot

```bash
# Download Godot .NET from https://godotengine.org/download
wget https://github.com/godotengine/godot/releases/download/4.4-stable/Godot_v4.4-stable_mono_linux_x86_64.zip
unzip Godot_v4.4-stable_mono_linux_x86_64.zip -d ~/Software/Godot/
# Make sure godot is on PATH
export PATH="$HOME/Software/Godot:$PATH"
```

## 2. Install godot-mcp

```bash
git clone https://github.com/tugcantopaloglu/godot-mcp.git
cd godot-mcp
npm install && npm run build
```

## 3. Install mcp-proxy (for HTTP bridge)

```bash
npx mcp-proxy --transport streamable-http http://127.0.0.1:14095/mcp
```

## 4. Configure AI Assistant

Add to your Hermes config (`~/.hermes/config.yaml`):

```yaml
mcp_servers:
  godot:
    url: "http://127.0.0.1:14095/mcp"  # or via SSH tunnel
    env:
      GODOT_PATH: "/usr/local/bin/godot"
```

## 5. Python Training Environment

```bash
uv venv .venv
source .venv/bin/activate
uv pip install godot-rl
```

## Remote Setup

When Godot is not on the same machine as the AI assistant:

```bash
# On control machine: establish SSH tunnel
ssh -L 14095:127.0.0.1:14095 user@target-device

# On target device: start MCP server
tmux new-session -d -s godot-mcp 'node /path/to/godot-mcp/build/index.js'
```

## Device Profile

Copy `templates/device-profile-template.sh` to `configs/device-<name>.sh`
and fill in the fields:

```bash
DEVICE_NAME="my-machine"
DEVICE_ROLE="dev+train"
SSH_HOST="192.168.1.100"
SSH_PORT=22
SSH_USER="myuser"
GODOT_PATH="/usr/local/bin/godot"
GODOT_DOTNET=true
MCP_ENABLED=true
HAS_GPU=true
PYTHON_ENV="uv"
```
