# Godot Agentic Toolkits — Development Roadmap

> Living roadmap. Updated as direction evolves.
> See docs/ARCHITECTURE.md for architecture decisions.

---

## Phase 1 — Foundation Polish ✅ DONE

| # | Task | Status |
|:-:|:-----|:------:|
| 1.1 | Review `godot-agentic` skill (MCP tool names, remote SSH instructions) | ✅ PR #1 merged |
| 1.2 | Review `godot-marl-dev` skill (RL Agents setup, SB3 training commands) | ✅ PR #2 merged |
| 1.3 | Write `language-programming-skills/README.md` | ✅ Gitea PR #1 |
| 1.4 | Write `CONTRIBUTING.md` (PR workflow, commit conventions) | ✅ PR #3 merged |
| 1.5 | Dual-copy sync script | 🗑️ Skipped |
| 1.6 | `.editorconfig` (BSD/Allman style) | ✅ PR #4 merged |
| 1.7 | `docs/ARCHITECTURE.md` | ✅ Drafted |
| 1.8 | Device profile template | ✅ `templates/device-profile-template.sh` |

---

## Phase 2 — Device Validation

**Goal:** Validate the development pipeline on a real remote machine.
Set up a development machine with Godot + MCP server, test scene editing,
C# build, and short smoke tests. Training workflow follows in Phase 3+.

### 2.0 — Architecture & Tooling (CURRENT)

| # | Task |
|:-:|:-----|
| 2.0.1 | ~~✅ Write ARCHITECTURE.md~~ |
| 2.0.2 | Write device profile for first development machine (local only) |
| 2.0.3 | Update AGENTS.md to reference ARCHITECTURE.md |

### 2.1 — MCP Server Deployment

| # | Task |
|:-:|:-----|
| 2.1.1 | SSH to target, check Node.js version |
| 2.1.2 | Install tugcantopaloglu/godot-mcp |
| 2.1.3 | Install mcp-proxy |
| 2.1.4 | Write device profile |
| 2.1.5 | Verify: `godot-mcp --version` |

### 2.2 — MCP Connectivity

| # | Task |
|:-:|:-----|
| 2.2.1 | Register MCP server in AI assistant config |
| 2.2.2 | Establish SSH tunnel (start-tunnel.sh) |
| 2.2.3 | Test: MCP connection |
| 2.2.4 | Test: `get_godot_version` via MCP |

### 2.3 — Basic Operations

| # | Task |
|:-:|:-----|
| 2.3.1 | `create_project(dotnet: true)` — scaffold C# Godot project |
| 2.3.2 | `create_csharp_script` — template generation |
| 2.3.3 | Write basic agent script by hand |
| 2.3.4 | `dotnet build` via SSH — compilation pass |

### 2.4 — Training Smoke Test

| # | Task |
|:-:|:-----|
| 2.4.1 | Set up Python environment |
| 2.4.2 | Short SB3 PPO training run (~100 steps) |
| 2.4.3 | TensorBoard SSH forwarding |
| 2.4.4 | ONNX export → verify model file |

---

## Phase 3 — Content Expansion

**Goal:** Fill gaps and add RL backends.

| # | Task |
|:-:|:-----|
| 3.1 | CleanRL training template |
| 3.2 | SampleFactory training template |
| 3.3 | Multi-agent example tutorial |
| 3.4 | C# skill: add Godot-specific section |
| 3.5 | godot-agentic references/ expansion |

---

## Phase 4 — Quality & Sustainability

**Goal:** Make the toolkit maintainable by contributors.

| # | Task |
|:-:|:-----|
| 4.1 | CI: skill content validation |
| 4.2 | CI: script shellcheck |
| 4.3 | CI: Godot project template `dotnet build` |
| 4.4 | Godot Asset Library submission |

---

## Key Constraints

- **Everything must work remotely** — Godot may be on a different machine
  than the AI assistant. No assumption of local Godot.
- **Device-agnostic** — new devices need only a config profile, not
  architecture changes. See `docs/ARCHITECTURE.md`.
- **C# support is non-negotiable** — Godot RL Agents requires .NET build.
- **MIT license** — matches Godot, RL Agents, godot-mcp ecosystems.
