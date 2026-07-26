# Skills Reference

This project defines two composable skills for AI agents:

## godot-agentic

**Layer 2** — General Godot engine development.

| Feature | Details |
|:--------|:--------|
| **Scope** | CLI, scene editing, project management, build/export |
| **MCP Tools** | 157 tools via tugcantopaloglu/godot-mcp v3.1.0+ |
| **Languages** | C# / GDScript (references language skills externally) |
| **Remote** | SSH tunnel setup, MCP configuration |

Triggers: `godot`, `game development`, `scene`, `godot project`

### Key Topics

- Godot engine CLI (`godot --headless --script`, export pipeline)
- Scene editing via MCP (create_scene, add_node, read_scene, get_scene_tree)
- Project scaffolding and configuration
- MCP server connection and troubleshooting

## godot-marl-dev

**Layer 3** — Multi-Agent Reinforcement Learning.

| Feature | Details |
|:--------|:--------|
| **Scope** | RL Agents plugin, training pipeline, multi-agent patterns |
| **Frameworks** | StableBaselines3 (SB3), CleanRL, SampleFactory |
| **Backends** | Configurable via `godot-rl` Python package |
| **Export** | ONNX model export and deployment |

Triggers: `reinforcement learning`, `MARL`, `multi-agent`, `godot rl agents`, `training`, `sb3`

### Key Topics

- Godot RL Agents plugin installation and SyncNode configuration
- Training loop: Godot as subprocess, observation/action/reward cycle
- Multi-agent patterns: Team, Adversarial, Self-play
- Model export: train → ONNX → Godot import

## How to Load

```bash
# In Hermes, these skills auto-load on triggers.
# Or load manually when starting a Godot-related session:
skill_view(name='godot-agentic')
```

For language-specific coding conventions, also load one of:
- `csharp-programming`
- `gdscript-programming`
- `python-programming`
