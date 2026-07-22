# Godot CLI Cheatsheet (Remote / Headless)

> Commands for operating Godot remotely via SSH.
> Godot must be a .NET build for C# projects.

---

## Basics

```bash
# Version check
godot --version

# List available export presets
godot --headless --export-list --path /path/to/project

# Command help
godot --help
```

---

## Headless Commands

Run Godot without a display server (no window, no GPU renderer):

```bash
# Validate a project (check for errors, no GPU needed)
godot --headless --path /path/to/project --check-only

# Run a single GDScript (.gd) headlessly
godot --headless --script path/to/script.gd

# Run the project headlessly (play mode, no window)
godot --headless --path /path/to/project

# Run with debug output
godot --headless --path /path/to/project --debug
```

### Headless Caveats

- `--headless` uses a **null rendering device** — no OpenGL/Vulkan context
- Scripts accessing `DisplayServer` or `RenderingServer` directly may error
- Physics and process loops run normally
- C# scripts work in headless mode (requires Godot .NET build)
- Performance is **better than windowed** (no vsync, no buffer swap)

---

## Export Pipeline

```bash
# Export for a specific preset (release)
godot --headless --export-release "Linux/X11" /tmp/build/Game.x86_64

# Export for debug
godot --headless --export-debug "Linux/X11" /tmp/build/Game.x86_64

# Export Windows build from Linux
godot --headless --export-release "Windows Desktop" /tmp/build/Game.exe

# Export with verbose logging
godot --headless --export-release "Linux/X11" /tmp/build/Game.x86_64 --verbose
```

### Common Preset Names

| Platform | Preset Name |
|----------|-------------|
| Linux | `Linux/X11` |
| Windows | `Windows Desktop` |
| macOS | `macOS` |
| Web | `Web` |
| Android | `Android` |

**Presets must be configured in the Godot editor first** (or via `manage_export_presets`).

---

## Remote Execution (SSH Workflow)

```bash
# === Basic SSH ===
ssh user@target "cd /path/to/project && godot --headless --check-only"

# === Run training headlessly on GPU machine ===
ssh gpu-machine "
  cd ~/Projects/godot-training
  uv run python train_sb3.py --env_path /path/to/game.x86_64
"

# === tmux approach (preferred for long runs) ===
ssh gpu-machine "
  tmux new-session -d -s train \
    'cd ~/Projects && uv run python train_sb3.py'
"
# Reattach:
ssh -t gpu-machine "tmux attach -t train"
```

---

## dotnet Build

```bash
# Build the C# project
dotnet build

# Build with specific configuration
dotnet build -c Release

# Build with warnings as errors
dotnet build -warnaserror

# Clean build artifacts
dotnet clean && dotnet build

# Restore NuGet packages only
dotnet restore

# Build on a remote device via SSH
ssh target "cd ~/Projects/marl-runner && dotnet build"
```

### Godot .NET SDK

```xml
<Project Sdk="Godot.NET.Sdk/4.6.2">
  <PropertyGroup>
    <TargetFramework>net8.0</TargetFramework>
    <RootNamespace>MyGame</RootNamespace>
  </PropertyGroup>
</Project>
```

- **SDK version** must match Godot Engine version
- **TargetFramework**: Godot 4.x uses `net8.0`
- After C# edits: always rebuild (`dotnet build`) before running
- Build output: `.godot/mono/temp/bin/Debug/`

---

## Useful Environment Variables

| Variable | Effect |
|----------|--------|
| `GODOT_HEADLESS_NO_GRAPHICS=true` | Force no graphics even if display available |
| `DISPLAY=:99` | Point to Xvfb virtual display (CI servers) |
| `GODOT_PATH` | Used by godot-mcp to locate the engine binary |
| `GODOT_MCP_ALLOWED_DIRS` | Restrict MCP file access to specific paths |

### Using Xvfb for CI

```bash
# Start virtual display
Xvfb :99 -screen 0 1024x768x24 &
export DISPLAY=:99

# Godot can now run without a physical display
godot --path /project --check-only
```

---

## Project Validation

```bash
# Check project for errors (no export)
godot --headless --path /project --check-only
# Exit code: 0 = clean, non-zero = errors

# C# compilation
dotnet build
# Godot .NET errors show up here
```

---

## Resource UID Management

```bash
# Regenerate UIDs after file moves
godot --headless --path /project --editor
# Godot rebuilds UIDs on editor startup
```

---

## Performance Profiling (CLI)

```bash
# Print frame timing to stdout
godot --path /project --profiling

# Headless + profiling for minimal overhead
godot --headless --path /project --profiling --time-scale 2.0

# Capture to file
godot --headless --path /project --profiling 2>&1 | tee profile.log
```
