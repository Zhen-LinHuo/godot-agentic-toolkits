# Troubleshooting

## MCP Connection Issues

### Cannot connect to godot-mcp

```
Error: connect ECONNREFUSED 127.0.0.1:14095
```

**Check:**
1. Is the MCP server running on the target device?
   ```bash
   ps aux | grep godot-mcp
   ```
2. Is the SSH tunnel alive?
   ```bash
   ss -tlnp | grep 14095
   ```
3. Is the port correct in Hermes config?

### Tunnel keeps dropping

Add keepalive to SSH:
```bash
ssh -o ServerAliveInterval=30 -o ServerAliveCountMax=3 \
    -L 14095:127.0.0.1:14095 user@target-device
```

## Godot Issues

### Godot .NET not found

```bash
# Verify .NET edition
godot --version         # should show Mono-enabled
ls $(which godot)       # check if it's the Mono build
```

Install the **.NET edition** from:
https://godotengine.org/download/

### dotnet build fails

```bash
# Check .NET SDK
dotnet --list-sdks

# Restore Godot workload
dotnet workload install godot

# Restore NuGet packages
cd path/to/project
dotnet restore
```

## Training Issues

### godot-rl not found

```bash
# Activate Python environment
source .venv/bin/activate

# Install
uv pip install godot-rl
```

### GPU not detected

```bash
# Check CUDA
nvidia-smi

# Check PyTorch
python -c "import torch; print(torch.cuda.is_available())"
```

## Permission Issues

### SSH permission denied

```bash
# Check key permissions
chmod 600 ~/.ssh/id_ed25519

# Test connection
ssh -v user@host
```

### Git push fails

Ensure correct GitHub account:
```bash
gh auth status
# Should show Zhen-LinHuo account active for this repo
```

## See Also

- `docs/ARCHITECTURE.md` for connection patterns
- `scripts/start-tunnel.sh` for tunnel setup
- GitHub Issues: https://github.com/Zhen-LinHuo/godot-agentic-toolkits/issues
