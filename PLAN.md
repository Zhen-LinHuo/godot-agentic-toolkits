# Godot Agentic Toolkits — Development Roadmap

> Living roadmap. Updated as direction evolves.
> See AGENTS.md for agent development guide.

## Current State (2026-07-20)

**Initial skeleton deployed.** Two skills (`godot-agentic`, `godot-marl-dev`),
four programming language skills, SSH tunnel scripts, and basic MARL project
template committed. All on `develop`, not yet reviewed.

**Notable gaps:**
- File-level refs structure per skill mostly empty (placeholder dirs)
- Remote tunnel scripts work but parameterisation may need refinement on first real use
- MARL training template uses SB3 only — CleanRL/SampleFactory stubs needed
- RL Agents plugin setup steps in godot-marl-dev are based on docs, not yet tested with a real project
- No CI/CD for skill quality checks
- ~/.hermes-dev/repos/ dual-copy sync script not yet written

---

## Phase 1 — Foundation Polish

**Goal:** Review and harden existing content before any feature work.

| # | Task | Description |
|---|------|-------------|
| 1.1 | Review `godot-agentic` SKILL.md | Verify MCP tool names, command examples, remote SSH tunnel instructions against actual godot-mcp v3.1 |
| 1.2 | Review `godot-marl-dev` SKILL.md | Verify RL Agents plugin setup steps, SB3 training command structure |
| 1.3 | Write `language-programming-skills/README.md` | Project overview, skill list, cross-reference guide |
| 1.4 | Write `godot-agentic-toolkits/CONTRIBUTING.md` | PR workflow, commit conventions, review checklist |
| 1.5 | Create dual-copy sync script | `scripts/sync-private.sh` — pull main into ~/.hermes-dev/repos/ |
| 1.6 | Set up `.editorconfig` at project root | Enforce BSD/Allman style for C#, Python, etc. |

**Device constraint:** remote tunnel scripts verified once a target device is available.

---

## Phase 2 — Device Validation

**Goal:** Test the full pipeline end-to-end on an actual remote device.

| # | Task | Description |
|---|------|-------------|
| 2.1 | Deploy on target device | Install godot-mcp, Node.js, mcp-proxy |
| 2.2 | SSH tunnel test | Verify Hermes ↔ target connectivity through start-tunnel.sh |
| 2.3 | Basic Godot ops via MCP | call `get_godot_version`, `create_project(dotnet: true)`, `create_csharp_script` |
| 2.4 | First training smoke test | Template → project → RL Agents sync → SB3 training → metrics visible |

---

## Phase 3 — Content Expansion

**Goal:** Fill gaps and add RL backends.

| # | Task | Description |
|---|------|-------------|
| 3.1 | CleanRL training template | `templates/training/cleanrl_ppo.py` |
| 3.2 | SampleFactory template | `templates/training/sample_factory_*.py` |
| 3.3 | Multi-agent example | Tutorial-level example: two teams competing |
| 3.4 | C# skill: add Godot-specific section | DotNet build patterns, partial class, signal interop |
| 3.5 | godot-agentic refs: expand | Scene tree patterns, export preset reference, common node configs |

---

## Phase 4 — Quality & Sustainability

**Goal:** Make the toolkit maintainable by contributors other than the original author.

| # | Task | Description |
|---|------|-------------|
| 4.1 | CI: skill content validation | Check frontmatter, unique tool names, valid references |
| 4.2 | CI: script shellcheck | Lint shell scripts |
| 4.3 | CI: Godot project template validation | `dotnet build` on template |
| 4.4 | Godot Asset Library submission | Package godot-agentic skill for discoverability |

---

## Key Constraints

- **Everything must work remotely** — Godot may be on a different machine than the AI assistant. No assumption of local Godot.
- **C# support is non-negotiable** — Godot RL Agents plugin requires Godot .NET build
- **Layer 1 skills use fuzzy cross-references** — no hardcoded skill names in godot-agentic or godot-marl-dev
- **MIT license** — matches Godot, RL Agents, godot-mcp ecosystems
