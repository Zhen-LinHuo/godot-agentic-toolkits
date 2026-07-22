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
├── docs/             # Architecture and workflow docs
└── AGENTS.md         # This file
```

> See `docs/ARCHITECTURE.md` for multi-device remote architecture,
> connection patterns, and operation routing.

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

This repository follows a **strict PR-based workflow**. Direct pushes to `main` are
forbidden — all changes go through feature branches → PR → merge.

### Branch Strategy

```
main       ← PR merges only (protected via convention)
develop    ← daily development, branch here for new work
<type>/<description>  ← feature/fix branches from develop
```

| Branch | Purpose | Push policy |
|--------|---------|------------|
| `main` | Stable release, consumed by ~/.hermes-dev/repos/ | PR merge only |
| `develop` | Active development, integration branch | Free push |
| `<type>/<desc>` | Individual features/fixes | Free push, PR into develop → main |

### Workflow

```text
1. git checkout develop && git pull
2. git checkout -b <type>/<description>     # e.g. feat/add-tunnel-auth
3. Commit with Conventional Commits format
4. git push origin <type>/<description>
5. Create PR from branch → develop (or main for releases)
6. After merge: switch to develop, pull, delete local branch
```

### Commit Conventions (Conventional Commits)

```
<type>: <imperative description, lowercase, ≤72 chars>
```

- Types: `feat`, `fix`, `docs`, `refactor`, `chore`, `test`, `perf`, `ci`
- One commit = one logical change — if you need `and`/`also` in the title, split
- Body explains WHY (root cause, context), not WHAT (diff shows that)
- No "Phase X" labels in commit messages

### Dual-Copy Pattern

```
~/Projects/hermes-dev/<repo>/     → develop copy (pushes to remote)
~/.hermes-dev/repos/<repo>/       → private copy (tracks main, never pushes)
```

After a PR merges to main:
```bash
cd ~/.hermes-dev/repos/<repo>
git pull origin main
```

### Git Identity

This repo uses per-repository identity, not global:

```bash
git config user.name "Zhen-LinHuo"
git config user.email "zhenlinhuo@gmx.com"
```
