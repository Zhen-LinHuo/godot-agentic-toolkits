# Godot Agentic Toolkits

**AI-assisted Godot development environment — scene editing, C# scripting, MARL training, and remote orchestration.**

A toolkit for AI agents (Hermes Agent, Claude Code, Codex, etc.) to work with the Godot game engine, with a focus on:

- **General Godot development** — scene editing, project scaffolding, C#/GDScript coding
- **Multi-Agent Reinforcement Learning (MARL)** — Godot RL Agents plugin integration, training pipeline, multi-agent patterns
- **Remote development** — Godot runs on one machine, AI assistant on another via SSH tunnel

## Quick Links

| | |
|:--|:--|
| 🏠 [Wiki Home](docs/wiki/Home.md) | Entry point for all documentation |
| 🏗️ [Architecture](docs/wiki/Architecture.md) | Multi-device remote architecture |
| 🔧 [Setup Guide](docs/wiki/Setup-Guide.md) | Install Godot + MCP + training env |
| 📘 [Skills Reference](docs/wiki/Skills-Reference.md) | Using `godot-agentic` and `godot-marl-dev` |
| 🔄 [Workflow](docs/wiki/Development-Workflow.md) | Daily development loops |

## Architecture

```
AI Agent ── MCP ──▶ godot-mcp (157 tools) ──▶ Godot (CLI + Runtime)
                          │
                    SSH tunnel ──▶ Target Device
```

Godot runs on a remote machine; the AI assistant connects via SSH tunnel.
See [Architecture](docs/wiki/Architecture.md) for connection patterns.

## Skills

This project provides two composable Hermes skills:

- **[godot-agentic](skills/godot-agentic/SKILL.md)** — Godot engine development: MCP setup, scene editing, project management, build/export. Language-agnostic foundation.
- **[godot-marl-dev](skills/godot-marl-dev/SKILL.md)** — MARL-specific workflow: RL Agents plugin, training pipeline (SB3/CleanRL/SampleFactory), multi-agent patterns, ONNX deployment.

## Contents

| Path | Description |
|:-----|:------------|
| `skills/godot-agentic/` | Layer 2 skill — general Godot development |
| `skills/godot-marl-dev/` | Layer 3 skill — MARL with Godot RL Agents |
| `scripts/` | Remote setup, tunnel, training launcher scripts |
| `templates/` | Project scaffolding and code templates |
| `configs/` | MCP config samples, device profiles (local-only) |
| `docs/` | Architecture and workflow documentation |
| `docs/wiki/` | Wiki-style documentation (will sync to GitHub Wiki) |

## References

- [Godot Engine](https://godotengine.org/) — MIT licensed
- [Godot RL Agents](https://github.com/edbeeching/godot_rl_agents) — Beeching et al., AAAI-2022 Workshop. [arXiv:2112.03636](https://arxiv.org/abs/2112.03636)
- [tugcantopaloglu/godot-mcp](https://github.com/tugcantopaloglu/godot-mcp) — MIT licensed, 157 MCP tools for Godot 4.x
- [Model Context Protocol](https://modelcontextprotocol.io/) — Open standard

## License

MIT — see [LICENSE](LICENSE).
