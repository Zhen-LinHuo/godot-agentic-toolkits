# Godot Agentic Toolkits Wiki

Welcome to the **Godot Agentic Toolkits** wiki — a collection of guides,
references, and workflows for AI-assisted Godot development.

## Quick Links

| Page | Description |
|:-----|:------------|
| [Architecture](Architecture) | Multi-device remote architecture, connection patterns, deployment tiers |
| [Setup Guide](Setup-Guide) | Install Godot, MCP server, and configure a development device |
| [Skills Reference](Skills-Reference) | Using `godot-agentic` and `godot-marl-dev` Hermes skills |
| [Development Workflow](Development-Workflow) | Daily development loops, training, model export |
| [Device Profiles](Device-Profiles) | How to configure new remote devices |
| [Troubleshooting](Troubleshooting) | Common issues and fixes |

## About This Project

[Godot Agentic Toolkits](https://github.com/Zhen-LinHuo/godot-agentic-toolkits)
provides skills, scripts, and templates for AI agents to work with the
Godot game engine — scene editing, C# scripting, multi-agent reinforcement
learning, and remote orchestration.

### Skill Architecture (3-Layer)

```
Layer 1: Language Programming Skills   (external, project-independent)
  — csharp-programming, gdscript-programming, python-programming, c-programming

Layer 2: godot-agentic                 (this project)
  — Godot engine CLI and MCP tools
  — Scene/project management
  — Language-agnostic Godot patterns

Layer 3: godot-marl-dev                (this project)
  — Godot RL Agents plugin integration
  — Training pipeline (SB3/CleanRL/SampleFactory)
  — Multi-agent patterns
  — ONNX export/deployment
```

### Project Structure

```
godot-agentic-toolkits/
├── skills/           # AI agent skills (SKILL.md + references/)
├── scripts/          # Remote setup, tunnel, training launchers
├── templates/        # Godot project, agent, training scaffolds
├── configs/          # MCP config samples, device profiles (local-only)
├── docs/             # Architecture and workflow documentation
└── AGENTS.md         # AI assistant configuration
```
