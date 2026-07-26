# Architecture

See [docs/ARCHITECTURE.md](https://github.com/Zhen-LinHuo/godot-agentic-toolkits/blob/develop/docs/ARCHITECTURE.md)
for the full architecture document. This page is a summary.

## High-Level Model

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
                                       ├── File operations
                                       └── Python training tasks
```

## Principles

1. **Control plane model** — AI assistant controls remote devices over SSH/MCP
2. **Device role separation** — separate dev, training, or combined machines
3. **Device profiles** — each device described by a config, no architecture changes
4. **Degradation transparency** — clear errors when capabilities are unavailable

## Connection Patterns

| Pattern | Use When |
|:--------|:---------|
| **Direct SSH** | Device is network-reachable (public IP, VPN, overlay) |
| **Reverse Tunnel** | Device is behind NAT (connects out with `-R`) |
| **Overlay Network** | Both machines on ZeroTier / Tailscale / NetBird |

## Deployment Tiers

| Capability | Full (L3) | Dev-only (L2) | Train-only (L1) | Minimal (L0) |
|:-----------|:---------:|:-------------:|:----------------:|:------------:|
| MCP server | ✅ | ✅ | ❌ | ❌ |
| Godot CLI | ✅ | ✅ | ❌ | ✅ |
| dotnet SDK | ✅ | ✅ | ❌ | ✅ |
| GPU + CUDA | ✅ | ❌ | ✅ | ❌ |
| RL training | ✅ | ❌ | ✅ | ❌ |

## Routing

| Operation | Target |
|:----------|:-------|
| C# code editing, dotnet build | Dev machine (Godot .NET) |
| Scene/node manipulation | Dev machine (MCP server) |
| Full-scale training | Training machine (GPU) |
| Model export (ONNX) | Training machine |
| Git/file ops | Fastest reachable device |
