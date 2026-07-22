# MCP Tools Quick Reference

> Quick-index for godot-mcp tools. All parameters use **camelCase**.
> `projectPath` is always an **absolute filesystem path**, not `res://`.

---

## Project Management

| Tool | Parameters | Description |
|------|-----------|-------------|
| `create_project` | `projectPath`, `projectName`, `dotnet` (bool) | Scaffold new Godot project |
| `get_project_info` | `projectPath` | Returns C# flag, Godot version |
| `list_project_files` | `projectPath`, `extension` (opt) | Filter by `.gd`, `.cs`, `.tscn` |
| `read_project_settings` | `projectPath` | Full project.godot as structured data |
| `modify_project_settings` | `projectPath`, `section`, `key`, `value` | Change any setting |

### Creating a Project

```
create_project(projectPath="/abs/path/to/project",
               projectName="MyGame",
               dotnet=true)
```

---

## Scene Management

| Tool | Parameters | Description |
|------|-----------|-------------|
| `create_scene` | `projectPath`, `scenePath`, `rootNodeType` | New scene with root type |
| `add_node` | `projectPath`, `scenePath`, `parentNodePath`, `nodeType`, `nodeName`, `properties` (dict) | Add child node |
| `remove_node` | `projectPath`, `scenePath`, `nodePath` | Remove node from scene |
| `read_scene` | `projectPath`, `scenePath` | Scene as structured JSON tree |
| `modify_scene_node` | `projectPath`, `scenePath`, `nodePath`, `properties` | Set node props |
| `save_scene` | `projectPath`, `scenePath`, `newPath` (opt) | Save (optionally as variant) |
| `duplicate_scene` | `projectPath`, `source`, `destination` | Copy scene file |
| `attach_script` | `projectPath`, `scenePath`, `nodePath`, `scriptPath` | Attach `.cs` or `.gd` script |
| `detach_script` | `projectPath`, `scenePath`, `nodePath` | Remove attached script |

### Scene Graph Navigation

```
Node
  └── root (.)
       ├── Player (CharacterBody2D)
       │    ├── Sprite (Sprite2D)
       │    └── Collision (CollisionShape2D)
       ├── UI (CanvasLayer)
       │    └── HUD (Control)
       └── World (Node2D)
            └── Enemies (Node)
```

Use `parentNodePath="."` to add under root.
Use `nodePath="Player"` to target a specific node.
Use `properties={"texture": "res://assets/sprite.png"}` for property setting.

---

## C# Script Tools

| Tool | Parameters | Description |
|------|-----------|-------------|
| `create_csharp_script` | `projectPath`, `scriptPath`, `className`, `baseClass`, `methods` | Scaffold a C# script |
| `create_script` | `projectPath`, `scriptPath`, `content` | Write GDScript directly |
| `validate_script` | `projectPath`, `scriptPath` | Check GDScript syntax |
| `validate_scripts` | `projectPath` | Batch-check all modified GDScripts |
| `update_project_uids` | `projectPath` | Refresh resource UIDs after file moves |

### C# Script Template

```json
create_csharp_script(projectPath="/path/to/project",
                     scriptPath="scripts/Player.cs",
                     className="Player",
                     baseClass="CharacterBody2D",
                     methods=["_Ready", "_Process", "_PhysicsProcess"])
```

Generates:
```csharp
using Godot;
using System;

public partial class Player : CharacterBody2D
{
    public override void _Ready() { }
    public override void _Process(double delta) { }
    public override void _PhysicsProcess(double delta) { }
}
```

---

## Editor & Launch

| Tool | Parameters | Description |
|------|-----------|-------------|
| `launch_editor` | `projectPath` | Open project in Godot editor |
| `run_project` | `projectPath` | Run in play mode |
| `stop_project` | — | Stop running project |
| `manage_export_presets` | `projectPath`, `action` (list/add/remove) | Manage export configs |
| `export_project` | `projectPath`, `presetName`, `outputPath` | Export to binary |
| `manage_plugins` | `projectPath`, `action` (list/enable/disable) | Manage editor plugins |

### Export Pipeline

```
1. manage_export_presets(path, action="list")
   → Check existing presets

2. manage_export_presets(path, action="add", presetName="Linux/X11")
   → Add preset if missing

3. export_project(path, presetName="Linux/X11",
                   outputPath="/tmp/build/Game.x86_64")
   → Export

4. Verify output file exists
```

---

## Runtime (Game Running)

| Tool | Parameters | Description |
|------|-----------|-------------|
| `game_eval` | `code` | Execute GDScript; prefix with `return` for values |
| `game_get_scene_tree` | — | Current scene tree as JSON |
| `game_get_property` | `nodePath`, `property` | Read runtime property |
| `game_set_property` | `nodePath`, `property`, `value` | Modify runtime property |
| `game_get_signal_list` | `nodePath` | Available signals on a node |
| `game_call_method` | `nodePath`, `method`, `args` | Call method at runtime |
| `game_pause` | `paused` (bool) | Pause/resume game |
| `game_get_errors` | — | Runtime error log |
| `game_get_logs` | — | Runtime console log |
| `game_screenshot` | — | Current frame as PNG |
| `game_performance` | — | FPS, memory, draw calls, physics |
| `game_connect_signal` | `nodePath`, `signalName`, `targetPath`, `method` | Dynamic signal connect |
| `game_time_scale` | `scale` (float) | Global time scale (slow-motion) |

**Prerequisite:** The MCP Interaction Server (`mcp_interaction_server.gd`) must be registered as an autoload in the project.

---

## Resource & File

| Tool | Parameters | Description |
|------|-----------|-------------|
| `open_folder` | `path` | Open directory in file manager |
| `open_in_explorer` | `path` | Open in OS file explorer |
| `read_file_text` | `path` | Read arbitrary file content |
| `write_file_text` | `path`, `content` | Write arbitrary file |

---

## Common Workflows

### New C# Project from Scratch

```
1. create_project(path="...", name="MyGame", dotnet=true)
2. create_csharp_script(path="...", scriptPath="scripts/Player.cs",
                         className="Player", baseClass="CharacterBody2D")
3. create_scene(path="...", scenePath="scenes/main.tscn",
                 rootNodeType="Node2D")
4. add_node(path="...", scenePath="scenes/main.tscn",
             parentNodePath=".", nodeType="CharacterBody2D",
             nodeName="Player")
5. attach_script(path="...", scenePath="scenes/main.tscn",
                  nodePath="Player", scriptPath="res://scripts/Player.cs")
```

### Iterative Edit → Build Cycle

```
1. modify_scene_node(...) or modify_project_settings(...)
2. dotnet build (via SSH)
3. run_project(path="...") or launch_editor(path="...")
4. game_get_errors() → check for runtime issues
5. game_performance() → verify no regression
```

### Debugging a Running Game

```
game_get_scene_tree()
  → Inspect node structure
game_get_property(nodePath="/root/Main/Player", property="position")
  → Check runtime values
game_eval(code="return get_tree().current_scene.debug_info()")
  → Custom runtime introspection
game_get_errors()
  → Full error log
```

---

## Parameter Pattern Summary

| Pattern | Examples |
|---------|----------|
| Paths: Absolute, not `res://` | `"/home/user/projects/MyProject"` |
| Scene refs: Relative to project | `"scenes/main.tscn"` |
| Node paths: Dot-notation | `".", "Player", "UI/HUD/HealthBar"` |
| Properties: Dict of key-value | `{"position": Vector2(100, 200)}` |
| Methods: List of strings | `["_Ready", "_Process"]` |
| Actions: Enum strings | `"list", "add", "remove", "enable", "disable"` |
