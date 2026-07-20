# Contributing

Thanks for contributing to Godot Agentic Toolkits!

This project follows a **strict PR-based workflow**. No direct pushes to `main`.
All changes go through feature branches → pull request → merge.

---

## Quick Start

```bash
git clone https://github.com/Zhen-LinHuo/godot-agentic-toolkits.git
cd godot-agentic-toolkits
git checkout develop
```

---

## Branch Strategy

```
main              ← PR merges only (protected by convention)
  └─ develop      ← daily development, branch here
       ├─ feat/<description>     → new features
       ├─ fix/<description>      → bug fixes
       ├─ docs/<description>     → documentation changes
       ├─ refactor/<description> → code restructuring
       ├─ chore/<description>    → maintenance, tooling, config
       └─ test/<description>     → test additions or fixes
```

| Branch | Push policy | Description |
|--------|------------|-------------|
| `main` | PR merge only | Stable release. Consumed by `~/.hermes-dev/repos/` |
| `develop` | Free push | Active development, integration branch |
| `<type>/<desc>` | Free push | Individual features/fixes. PR into `develop` → `main` |

---

## Workflow

### 1. Start from develop

```bash
git checkout develop
git pull origin develop
```

### 2. Create a feature branch

```bash
git checkout -b <type>/<short-description>
```

Branch names use kebab-case: `fix/godot-agentic-mcp-params`, `docs/contributing-guide`.

### 3. Commit

Write commits in [Conventional Commits](https://www.conventionalcommits.org/) format (see below).
Keep commits logically separated — one logical change per commit.

### 4. Push

```bash
git push origin <type>/<description>
```

### 5. Create a pull request

Open a PR from your branch into `develop`.
GitHub will show the comparison automatically if you push before creating the PR.

### 6. Review and merge

- Self-review your own diff first
- Check that all items in the review checklist below pass
- Merge via **squash merge** to keep `develop` history clean
- Delete the feature branch after merge

### 7. Sync private copy (if applicable)

```bash
cd ~/.hermes-dev/repos/godot-agentic-toolkits
git pull origin main
```

---

## Commit Conventions

### Format

```
<type>: <imperative description, lowercase, ≤72 chars>

<optional body: explain WHY, not WHAT>
```

Types:
- `feat:` — new feature
- `fix:` — bug fix
- `docs:` — documentation only
- `refactor:` — code restructuring with no functional change
- `chore:` — maintenance, tooling, config changes
- `test:` — adding or fixing tests
- `perf:` — performance improvement
- `ci:` — CI/CD changes

### Rules

- **One commit = one logical change.** If the title needs `and`/`also`, split the commit.
- **Imperative mood.** `fix: correct MCP tool parameter names` not `fixed` or `fixes`.
- **Lowercase.** No leading capitalisation on the description.
- **Body explains WHY**, not WHAT. The diff already shows what changed.
- **No "Phase X" labels** in commit messages.
- **Same-session separation.** A `docs:` update and a `feat:` addition in the same session are separate commits.

### Examples

```text
Good:
  feat: add CleanRL training template
  fix: correct projectPath parameter name in create_scene example
  docs: add CONTRIBUTING.md with PR workflow

Avoid:
  feat: Add CleanRL training template       ← capitalised
  fix: corrected param names and added docs ← two things in one commit
  chore: Phase 1 polish                     ← phase labels in messages
```

---

## Review Checklist

Before submitting or merging a PR, check:

- [ ] **Commits** — Conventional Commits format, logically separated, no phase labels
- [ ] **SKILL.md validity** — if changed, verify tool/parameter names against actual source
- [ ] **Cross-references** — Layer 1 skill references use fuzzy descriptions (not hardcoded skill names)
- [ ] **README/AGENTS.md** — updated if the PR changes how the project is used
- [ ] **No credentials** — no passwords, tokens, API keys in any file
- [ ] **No stale planning artifacts** — PLAN.md entries updated or removed, no TODO/FIXME left in code

---

## Git Identity

This repo uses per-repository identity:

```bash
git config user.name "Zhen-LinHuo"
git config user.email "zhenlinhuo@gmx.com"
```

Do not set these globally — they are specific to this project.

---

## Getting Help

Open an issue on GitHub or start a discussion.
