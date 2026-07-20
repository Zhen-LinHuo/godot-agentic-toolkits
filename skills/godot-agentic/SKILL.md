---
name: godot-agentic
description: "Godot game engine development — MCP server setup, scene/project management, C#/GDScript coding, build pipeline. Language-agnostic foundation for AI-assisted Godot development."
version: 0.1.0
author: Zhen-LinHuo
tags:
  - godot
  - game-development
  - scene-editing
  - csharp
  - gdscript
triggers:
  - godot
  - game development
  - scene
  - godot project
---

# godot-agentic

> This skill covers **general Godot engine development** — project scaffolding,
> scene editing, C#/GDScript coding, build/export, and MCP tool integration.
>
> For MARL-specific workflows (RL Agents, training pipeline), see `godot-marl-dev`.
> For language-specific programming conventions, load a language programming skill
> (see references below).

---

## Prerequisites

### Required: Godot Engine
- Godot **4.4+** (4.7 recommended), **.NET/C# version** for C# projects
- The Godot engine can run **locally or on a remote device** (see Remote Setup)

### Required: MCP Server
- [tugcantopaloglu/godot-mcp](https://github.com/tugcantopaloglu/godot-mcp) v3.1.0+
- Node.js >= 18 on the machine running the MCP server
- 157 tools available: scene ops, project management, runtime interaction, 3D/2D, audio, networking, animation, UI, physics

### Optional: Language Programming Skills
When writing code in a specific language, load a programming skill if one is available:

- **C#** → A C# programming skill (naming conventions, project structure, .NET SDK patterns, common pitfalls)
- **GDScript** → A GDScript programming skill (Godot scripting conventions, static typing, signal patterns)
- **Python** → A Python programming skill (type annotations, uv/pip toolchain, testing conventions)

---

## Remote Setup (Godot on a Different Machine)

When Godot is not on the same machine as the AI assistant, use SSH tunnelling:

### Architecture

```
AI Assistant
    │ MCP (HTTP or stdio)
    ▼
MCP Server (Node.js)  ── SSH ──▶ Target Device
    │                             ├── Godot .NET Editor
    ├── SSH: godot --headless     ├── godot-mcp interaction server (TCP :9090)
    ├── SSH: TCP tunnel :14095    └── dotnet SDK / Python venv
    └── SSH: dotnet build / run
```

### SSH Tunnel Setup

```bash
# On the machine running the AI assistant:
ssh -L 14095:127.0.0.1:14095 target-user@target-device
```

### MCP Server on Target Device

```bash
# On the target device (one-time):
git clone https://github.com/tugcantopaloglu/godot-mcp.git
cd godot-mcp
npm install && npm run build

# Start with HTTP bridge (tmux or systemd):
tmux new-session -d -s godot-mcp 'node build/index.js'
# Then mcp-proxy wraps stdio into HTTP:
npx mcp-proxy --transport streamable-http http://127.0.0.1:14095/mcp
```

### Hermes MCP Config

```yaml
# ~/.hermes/config.yaml
mcp_servers:
  godot:
    url: "http://127.0.0.1:14095/mcp"  # SSH tunnel local port
    env:
      GODOT_PATH: "/usr/local/bin/godot"  # path on target
      GODOT_MCP_ALLOWED_DIRS: "/home/user/projects"
```

### Health Check

```bash
# Verify tunnel:
curl http://127.0.0.1:14095/mcp
# Verify Godot reachable via MCP:
# → Ask the assistant to call get_godot_version or list_projects on a directory
```

---

## Godot CLI Reference

### Headless Commands

```bash
# Check version
godot --version

# Run a script headlessly (no window)
godot --headless --script path/to/script.gd

# Export project
godot --headless --export-release "Linux/X11" /path/to/output
godot --headless --export-debug "Windows Desktop" /path/to/output

# Run project (play mode)
godot --path /path/to/project

# Run with debug
godot --path /path/to/project --debug
```

### Project.godot Key Settings

| Setting | Key | Description |
|---------|-----|-------------|
| Main scene | `application/config/name` | Project display name |
| Main scene | `application/run/main_scene` | Default scene on run |
| Icon | `application/config/icon` | Project icon path |
| Version | `application/config/version` | Version string |

---

## MCP Tool Usage Patterns

> **Note:** All MCP tool parameters use **camelCase** (e.g. `projectPath`, `scenePath`, `rootNodeType`).
> `projectPath` is an **absolute filesystem path** to the Godot project directory (not a `res://` path).

### Scene Management

```json
// Create a new scene
create_scene(projectPath="/home/user/projects/MyGame",
             scenePath="scenes/main.tscn",
             rootNodeType="Node2D")

// Add a node to an existing scene
add_node(projectPath="/home/user/projects/MyGame",
         scenePath="scenes/main.tscn",
         parentNodePath=".",
         nodeType="Sprite2D",
         nodeName="Player",
         properties={"texture": "res://assets/player.png"})

// Read scene structure as JSON
read_scene(projectPath="/home/user/projects/MyGame",
           scenePath="scenes/main.tscn")

// Modify node properties in a scene file
modify_scene_node(projectPath="/home/user/projects/MyGame",
                  scenePath="scenes/main.tscn",
                  nodePath="Player",
                  properties={"position": Vector2(100, 200)})

// Save scene (optionally as variant)
save_scene(projectPath="/home/user/projects/MyGame",
           scenePath="scenes/main.tscn",
           newPath="scenes/main_variant.tscn")

// Attach a script to a scene node
attach_script(projectPath="/home/user/projects/MyGame",
              scenePath="scenes/main.tscn",
              nodePath="Player",
              scriptPath="res://scripts/player.gd")
```

### Project Management

```json
// Create a new C# Godot project
create_project(projectPath="/home/user/projects/MyGame",
               projectName="MyGame",
               dotnet=true)

// Get project info (reports isDotnet field)
get_project_info(projectPath="/home/user/projects/MyGame")

// Create a C# script
create_csharp_script(projectPath="/home/user/projects/MyGame",
                     scriptPath="scripts/PlayerController.cs",
                     className="PlayerController",
                     baseClass="CharacterBody2D",
                     methods=["_Ready", "_Process"])

// Create a GDScript file
create_script(projectPath="/home/user/projects/MyGame",
              scriptPath="scripts/enemy.gd",
              content="extends Node2D\nfunc _ready():\n    pass")

// Validate GDScript syntax
validate_script(projectPath="/home/user/projects/MyGame",
                scriptPath="scripts/player.gd")

// Batch-validate all changed GDScript files
validate_scripts(projectPath="/home/user/projects/MyGame")

// Read/manage project settings
read_project_settings(projectPath="/home/user/projects/MyGame")
modify_project_settings(projectPath="/home/user/projects/MyGame",
                        section="application/config",
                        key="name",
                        value="MyGame")

// List files in project
list_project_files(projectPath="/home/user/projects/MyGame",
                   extension=".gd")
```

### Editor & Export

```json
// Launch Godot editor for a project
launch_editor(projectPath="/home/user/projects/MyGame")

// Run the project
run_project(projectPath="/home/user/projects/MyGame")

// Stop the running project
stop_project()

// Manage export presets
manage_export_presets(projectPath="/home/user/projects/MyGame",
                      action="list")

// Export project
export_project(projectPath="/home/user/projects/MyGame",
               presetName="Linux/X11",
               outputPath="/tmp/build/MyGame.x86_64")

// Manage editor plugins
manage_plugins(projectPath="/home/user/projects/MyGame",
               action="list")
```

### Runtime Interaction (Game Running)

```json
// Execute GDScript in running game (use "return" for values)
game_eval(code="return get_tree().current_scene.name")

// Get scene tree structure
game_get_scene_tree()

// Get/modify property on a runtime node
game_get_property(nodePath="/root/Main/Player",
                  property="position")
game_set_property(nodePath="/root/Main/Player",
                  property="position",
                  value=Vector3(10, 0, 5))

// Call a method on a runtime node
game_call_method(nodePath="/root/Main/Player",
                 method="take_damage",
                 args=[10])

// Get performance metrics
game_performance()

// Pause/resume
game_pause(paused=true)

// Capture screenshot
game_screenshot()

// Connect/disconnect signals at runtime
game_connect_signal(nodePath="/root/Main/Player",
                    signalName="health_changed",
                    targetPath="/root/Main/UI",
                    method="on_health_changed")

// Get runtime logs and errors
game_get_errors()
game_get_logs()
```

### Common Workflows

#### Starting a New Godot C# Project

```
1. create_project(projectPath="...", projectName="...", dotnet=true)
     → scaffolds directory + .csproj + C# feature flag
2. create_csharp_script(projectPath="...", scriptPath="scripts/Main.cs",
                         className="Main", baseClass="Node2D")
     → generates C# partial class
3. create_scene(projectPath="...", scenePath="scenes/main.tscn",
                 rootNodeType="Node2D")
4. attach_script(projectPath="...", scenePath="scenes/main.tscn",
                  nodePath=".", scriptPath="res://scripts/Main.cs")
```

#### Project Export Pipeline

```
1. manage_export_presets(projectPath="...", action="list")  → check presets
2. manage_export_presets(projectPath="...", action="add", presetName="Linux/X11")
3. export_project(projectPath="...", presetName="Linux/X11",
                  outputPath="/tmp/build/MyGame.x86_64")
4. Verify output file exists
```

---

## Pitfalls & Known Issues

### Godot-MCP

- MCP server uses stdio by default; for remote use, wrap with `mcp-proxy` for HTTP transport
- Runtime tools (`game_*`) require the `mcp_interaction_server.gd` autoload registered in the project
- The TCP interaction server binds to `127.0.0.1:9090` by default (local only)

### Godot .NET / C#

- The C# version of Godot is a separate download — ensure the .NET build is installed
- `.csproj` must reference `Godot.NET.Sdk` matching the installed Godot version
- After script changes, the project must be rebuilt (`dotnet build`) before changes appear in the editor

### General

- Godot uses Resource UIDs (Godot 4.4+) — moving files externally can break references
- Always use `update_project_uids` after file moves if UID errors occur
- Scene file format is `.tscn` (text) or `.scn` (binary) — prefer `.tscn` for version control
