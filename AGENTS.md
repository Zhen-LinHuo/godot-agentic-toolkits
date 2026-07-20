# AGENTS.md — AI Assistant Configuration

This file tells AI coding assistants (Copilot, Codex, Claude Code, Hermes Agent, etc.)
how to work effectively with this repository.

## Repository Purpose

This is a **toolkit repository** — it contains skills, scripts, and templates
for AI-assisted Godot development. It is NOT a Godot project itself.

## Project Structure

```
godot-agentic-toolkits/
├── skills/           # AI agent skills (SKILL.md files)
├── scripts/          # Shell/setup scripts
├── templates/        # Project scaffolding
├── configs/          # MCP + SSH config samples
├── docs/             # Documentation
└── AGENTS.md         # This file
```

## Skill Architecture (3-Layer)

```
Layer 1: Language Programming Skills   (external, project-independent)
  — csharp-programming
  — gdscript-programming
  — python-programming
  — c-programming

Layer 2: godot-agentic  ← references Layer 1 via fuzzy description
  — Godot engine CLI and MCP tools
  — Scene/project management
  — Language-agnostic Godot patterns

Layer 3: godot-marl-dev  ← references Layer 2 + Layer 1
  — Godot RL Agents plugin integration
  — Training pipeline (SB3/CleanRL)
  — Multi-agent patterns
  — ONNX export/deployment
```

## Cross-Layer References

Skills in this repository refer to language programming skills (Layer 1) using
**fuzzy, generic descriptions** — not hardcoded skill names. This makes the
skills portable across different AI assistant environments where language
skills may have different names.

**Example:** Instead of "load csharp-programming skill", write:
> "When writing C# code, load a C# programming skill if one is available
> to get naming conventions, project structure patterns, and common pitfalls."

## Code Style

This project follows BSD/Allman style:
- **Braces**: Allman style (opening brace on its own line)
- **Indentation**: 4 spaces
- **Continuation**: Aligned with content after opening bracket/paren (not fixed indent)
- **C#**: Same style as C (Allman + aligned continuation), .editorconfig managed
- **Python**: Mandatory type annotations, uv toolchain
- **GDScript**: Godot official style (static typing, snake_case)

See `language-programming-skills` (Gitea: alrcatraz) for per-language skill definitions.

## Git Workflow

- This repository uses **standard git collaboration workflow** (feature branches, PRs)
- See CONTRIBUTING.md for detailed workflow
