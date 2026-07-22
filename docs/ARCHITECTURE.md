# Godot Agentic Toolkits — Remote Architecture

> This document defines the project's architecture for AI-assisted Godot
> development across remote devices. It describes concepts and patterns,
> not specific infrastructure.

---

## Architecture Model

```
Control Machine (AI Assistant)
        │
        ├── MCP Client ── SSH tunnel ──▶ Target Device: Godot MCP Server
        │                                      ├── Godot .NET (headless/editor)
        │                                      └── Scene/node editing via MCP tools
        │
        └── Terminal Tool ── SSH ──▶ Target Device(s)
                                           ├── dotnet build / test
                                           ├── Git operations
                                           ├── File operations (write, read, patch)
                                           └── Python training tasks
```

### Principles

1. **Control plane model** — the AI assistant runs on one machine (the
   "control machine") and operates remote devices over SSH/MCP. Devices
   are resources, not endpoints.

2. **Device role separation** — different devices may serve different
   roles in a project's lifecycle:
   - **Development machine**: code editing, scene editing via MCP,
     `dotnet build`, quick smoke tests. Needs Godot .NET + MCP server.
   - **Training machine**: large-scale RL training with GPU, model
     export. Needs Python + CUDA + RL framework. Does NOT need Godot GUI.
   - A single machine can fill both roles. The architecture supports
     splitting them when the workload scales.

3. **Degradation transparency** — the AI assistant checks device
   capabilities and routes operations to suitable targets. Unavailable
   operations produce clear errors, not silent failures.

4. **Device profiles** — each device is described by a configuration
   profile (connection method, installed software, capabilities). Adding
   a new device means adding a profile, not changing the architecture.

---

## Connection Patterns

### Direct SSH

```
Control Machine ──SSH──▶ Target Device
```

Prerequisite: target device is network-reachable from the control machine
(public IP, VPN, or overlay network).

Use for: development machines, any device that can accept inbound SSH.

### Reverse Tunnel

```
Target Device ──SSH -R──▶ Control Machine
                         (device connects out, no inbound port needed)
```

Prerequisite: device can initiate SSH to the control machine (e.g. via
SD-WAN overlay, VPN).

Use for: devices behind NAT that cannot accept inbound connections.
The device maintains the tunnel with keepalives; the AI assistant uses
the local end of the tunnel as if the device were directly reachable.

### Overlay Network (e.g. ZeroTier / NetBird / Tailscale)

```
Control Machine ──Overlay──▶ Target Device
```

Prerequisite: both machines on the same overlay network.

Use for: any device that can join the overlay. Provides encryption,
NAT traversal, and fixed virtual IPs regardless of physical network.

---

## Device Profile Specification

Each device has a key-value profile describing its identity and capabilities.
Profiles are stored locally on the control machine (never committed to the
project repository).

| Field | Required | Values | Description |
|-------|----------|--------|-------------|
| `DEVICE_NAME` | ✅ | string | Human-readable name |
| `DEVICE_ROLE` | ✅ | `dev` / `train` / `dev+train` / `check` | Intended use |
| `SSH_HOST` | ✅ | IP/hostname | SSH target |
| `SSH_PORT` | ✅ | number | SSH port |
| `SSH_USER` | ✅ | string | SSH login |
| `SSH_MODE` | ✅ | `direct` / `reverse` / `overlay` | Connection pattern |
| `GODOT_PATH` | ✅ | path | Path to Godot binary |
| `GODOT_DOTNET` | ✅ | boolean | .NET edition? |
| `MCP_ENABLED` | ✅ | boolean | godot-mcp installed? |
| `HAS_GPU` | ✅ | boolean | GPU available? |
| `PYTHON_ENV` | ❌ | `uv` / `conda` / `venv` | Python environment manager |

A template is available at `templates/device-profile-template.sh`.

---

## Operation Routing

The AI assistant routes operations based on device capabilities:

| Operation | Preferred target | Requirement |
|-----------|-----------------|-------------|
| C# code editing, dotnet build | Development machine | Godot .NET + dotnet SDK |
| Scene/node manipulation (MCP) | Development machine with godot-mcp | Node.js + godot-mcp |
| Short smoke-test training | Any device with Python | Python |
| Full-scale training (hours/days) | Training machine with GPU | Python + CUDA + RL framework |
| Model export (ONNX) | Training machine (same machine as training) | Python + onnx |
| Training monitoring (TensorBoard) | Control machine → SSH tunnel to training machine | Running training process |
| Model transfer to Godot project | scp/rsync training → dev machine | SSH |

### Routing decision flow

```
Operation requested
  ├─ MCP operation (scene/node) → needs MCP_ENABLED device
  │    ├─ online → execute via MCP
  │    └─ offline → error: MCP server unavailable
  ├─ Compile/validate → needs dotnet SDK
  │    ├─ dev machine online → use it
  │    └─ offline → error
  ├─ Training (full) → needs GPU
  │    ├─ training machine online → use it
  │    └─ offline → error (no fallback to non-GPU device)
  └─ Git/file ops → fastest SSH-reachable device
```

---

## Deployment Variance Tiers

| Capability | Full (L3) | Dev-only (L2) | Train-only (L1) | Minimal (L0) |
|------------|-----------|---------------|-----------------|---------------|
| MCP server | ✅ | ✅ | ❌ | ❌ |
| Godot CLI | ✅ | ✅ | ❌ | ✅ |
| dotnet SDK | ✅ | ✅ | ❌ | ✅ |
| GPU + CUDA | ✅ | ❌ | ✅ | ❌ |
| RL training | ✅ | ❌ | ✅ | ❌ |

A device profile declares its tier; the AI assistant respects it.

---

## Development Workflow (Example)

```
1. Code:    Write C# script → write_file → SSH dotnet build → fix errors → repeat
2. Scene:   MCP tools to create scene → add nodes → configure properties
3. Smoke:   Short training run on dev machine to verify RL integration
4. Deploy:  git-push code → on training machine: git-pull → launch full training
5. Monitor: SSH tunnel port-forward → TensorBoard on control machine browser
6. Export:  ONNX export on training machine → scp model to dev machine
7. Import:  Godot import ONNX file → MCP tools to attach to scene
```

---

## Project Repository

This repository (Zhen-LinHuo/godot-agentic-toolkits) contains:

| Path | Contents |
|------|----------|
| `scripts/` | Setup/tunnel scripts |
| `templates/` | Godot project, agent, training scaffolds |
| `configs/` | Configuration samples (device profiles are local-only) |
| `docs/` | Architecture and workflow documentation |
| `skills/` | AI assistant skill files |
| `AGENTS.md` | AI assistant configuration |
| `PLAN.md` | Development roadmap |
