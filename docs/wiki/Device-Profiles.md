# Device Profiles

Device profiles describe a remote machine's capabilities and connection
details. They are stored locally on the control machine and **never
committed to the repository** (they contain machine-specific addresses).

## Profile Format

```bash
# configs/device-<name>.sh
DEVICE_NAME="friendly-name"
DEVICE_ROLE="dev+train"        # dev / train / dev+train / check

# SSH
SSH_MODE="direct"              # direct / reverse / overlay
SSH_HOST="192.168.1.100"
SSH_PORT=22
SSH_USER="myuser"
SSH_AUTH="key"                 # password / key / askpass

# Overlay (optional)
OVERLAY_TYPE="netbird"         # netbird / zerotier / easytier
OVERLAY_IP="10.30.60.11"

# Godot
GODOT_PATH="/usr/local/bin/godot"
GODOT_DOTNET=true

# MCP
MCP_ENABLED=true
MCP_SERVER_PATH="/path/to/godot-mcp/build/index.js"

# Training
HAS_GPU=true
TRAINING_FRAMEWORKS="sb3"      # sb3 / cleanrl / samplefactory
PYTHON_ENV="uv"                # uv / conda / venv
```

## Using Profiles

```bash
source configs/device-my-machine.sh

# SSH with profile params
ssh -p $SSH_PORT $SSH_USER@$SSH_HOST "$GODOT_PATH --version"

# Establish MCP tunnel
ssh -L 14095:127.0.0.1:14095 -p $SSH_PORT $SSH_USER@$SSH_HOST
```

## Adding a New Device

1. Copy `templates/device-profile-template.sh` to `configs/device-<name>.sh`
2. Fill in the device's capabilities and connection details
3. Test: `source configs/device-<name>.sh && ssh $SSH_USER@$SSH_HOST "echo OK"`
4. Optionally register in Hermes for automatic routing

## Existing Profiles

See `configs/` directory for existing device profiles. Each profile is
named after the device's hostname.
