# Godot Agentic Toolkits

**AI-assisted Godot development environment — scene editing, C# scripting, MARL training, and remote orchestration.**

A toolkit for AI agents (Claude Code, Hermes Agent, Codex, etc.) to work with the Godot game engine, with a focus on:

- **General Godot development** — scene editing, project scaffolding, C#/GDScript coding
- **Multi-Agent Reinforcement Learning (MARL)** — Godot RL Agents plugin integration, training pipeline, multi-agent patterns
- **Remote development** — Godot runs on one machine (desktop, workstation, cloud), AI assistant on another

## Architecture

```
                         ┌─────────────────┐
                         │   AI Agent       │
                         │  (Hermes, Claude)│
                         └────────┬────────┘
                                  │ MCP (HTTP)
                                  ▼
                    ┌─────────────────────────┐
                    │   godot-mcp (MCP Server) │
                    │  157 tools               │
                    └────────┬────────┬────────┘
                             │        │
                    ┌────────▼─┐  ┌──▼─────────┐
                    │ Godot CLI │  │ Godot Runtime │
                    │ (headless) │  │ (TCP :9090)   │
                    └───────────┘  └──────────────┘
```

When Godot runs on a remote device, MCP communication goes through SSH tunnel or HTTP proxy.

## Contents

| Path | Description |
|:-----|:------------|
| `skills/godot-agentic/` | Layer 2 skill — general Godot development (project-agnostic) |
| `skills/godot-marl-dev/` | Layer 3 skill — MARL with Godot RL Agents (references godot-agentic) |
| `scripts/` | Remote setup, tunnel, training launcher scripts |
| `templates/` | Project scaffolding and code templates |
| `configs/` | Hermes MCP config samples, SSH config snippets |
| `docs/` | Architecture, setup, and workflow documentation |

## Skills in this Repository

This project defines two composable skills for AI agents:

1. **[godot-agentic](skills/godot-agentic/SKILL.md)** — Godot engine development: MCP setup, scene editing, project management, build/export. Language-agnostic foundation.

2. **[godot-marl-dev](skills/godot-marl-dev/SKILL.md)** — MARL-specific workflow: RL Agents plugin config, training pipeline (SB3/CleanRL/SampleFactory), multi-agent patterns, ONNX deployment. Builds on top of godot-agentic.

## Quick Start

*(Coming soon — device-dependent)*

## References & Inspiration

- [Godot Engine](https://godotengine.org/) — MIT licensed
- [Godot RL Agents](https://github.com/edbeeching/godot_rl_agents) — Edward Beeching et al., AAAI-2022 Workshop. [arXiv:2112.03636](https://arxiv.org/abs/2112.03636)
- [tugcantopaloglu/godot-mcp](https://github.com/tugcantopaloglu/godot-mcp) — MIT licensed, 157 MCP tools for Godot 4.x
- [Model Context Protocol](https://modelcontextprotocol.io/) — Open standard

## License

MIT — see [LICENSE](LICENSE).
