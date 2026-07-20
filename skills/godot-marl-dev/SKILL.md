---
name: godot-marl-dev
description: "Multi-Agent Reinforcement Learning with Godot — RL Agents plugin, training pipeline (SB3/CleanRL/SampleFactory), multi-agent patterns, ONNX export. References godot-agentic for general Godot operations."
version: 0.1.0
author: Zhen-LinHuo
tags:
  - godot
  - reinforcement-learning
  - MARL
  - multi-agent
  - training
  - SB3
triggers:
  - reinforcement learning
  - MARL
  - multi-agent
  - godot rl agents
  - training
  - sb3
---

# godot-marl-dev

> This skill covers **MARL-specific workflows** using Godot RL Agents.
> It builds on `godot-agentic` for general Godot operations.
>
> For other programming needs, load language-specific skills as needed:
> - **C#**: load a C# programming skill for naming conventions and project patterns
> - **Python**: load a Python programming skill for type annotations and toolchain conventions
> - **GDScript**: load a GDScript programming skill for Godot scripting patterns

---

## Overview

Godot RL Agents connects a Godot game (scene) to Python RL training frameworks.
The training loop:

```
Python Training Script (SB3/CleanRL/SampleFactory)
    │
    ├── Launches Godot as a subprocess (or connects to editor)
    ├── Sends actions  →  Godot steps the environment
    ├── Receives observations + rewards  ←  Godot sends back
    └── Trains policy  →  repeat
```

**Key repo:** [edbeeching/godot_rl_agents](https://github.com/edbeeching/godot_rl_agents) (MIT, ⭐1.5k)  
**Paper:** Beeching et al., AAAI-2022 Workshop. [arXiv:2112.03636](https://arxiv.org/abs/2112.03636)

---

## Setup

### 1. Install Godot RL Agents (Python side)

```bash
# On the training machine (e.g. ROG Strix with GPU):
pip install godot-rl   # or: uv pip install godot-rl
```

Supports four RL backends:
- **StableBaselines3** — Windows/Mac/Linux, easiest to start (default)
- **SampleFactory** — Mac/Linux, high-throughput
- **CleanRL** — Windows/Mac/Linux, hackable single-file implementation
- **Ray RLLib** — Windows/Mac/Linux, distributed training

### 2. Install Godot Plugin

The RL Agents plugin (C# 13% + GDScript 87%) must be installed in your Godot project:

```
# The plugin lives in the main repo as a submodule:
godot_rl_agents/
└── godot_rl_agents_plugin/  →  edbeeching/godot_rl_agents_plugin
    ├── addons/godot_rl_agents/     # Plugin source
    ├── Godot RL Agents.csproj      # C# project file
    └── Godot RL Agents.sln         # Solution file
```

Copy `addons/godot_rl_agents/` into your project's `addons/` directory,
then enable it in **Project → Project Settings → Plugins**.

**Important:** The plugin is a C# project — requires Godot .NET version.

### 3. Configure SyncNode

In your Godot scene, add a `Sync` node (provided by the plugin) that handles
communication between Godot and the Python training script:

- The `Sync` node manages observations, actions, and rewards
- Configure observation space (vector, image, or structured)
- Configure action space (discrete, continuous, or mixed)
- Attach your agent logic as a child script

### 4. Set Up the MCP Interaction Server (for Runtime Tools)

To use runtime MCP tools (`game_eval`, `game_set_property`, etc.) during training:

```bash
# Copy the interaction server from godot-mcp:
cp /path/to/godot-mcp/src/scripts/mcp_interaction_server.gd \
   your-project/scripts/

# Register as autoload in Godot:
# Project → Project Settings → Autoload → Add mcp_interaction_server.gd
```

---

## Training Pipeline

### Quick Start: SB3 Training

```bash
# 1. Export or use the Godot editor with --path
python examples/stable_baselines3_example.py \
    --env_path=/path/to/game.x86_64 \
    --experiment_name=Experiment_01 \
    --viz
```

For **in-editor training** (no export needed):
```bash
python examples/stable_baselines3_example.py
# The script auto-discovers the Godot editor via the project path
```

### Training Script Template

```python
# train_sb3.py — minimal training script
from godot_rl.core.godot_env import GodotEnv
from stable_baselines3 import PPO

def train():
    env = GodotEnv(
        env_path="path/to/game.x86_64",  # or None for editor
        seed=42,
        show_window=False                 # headless for speed
    )

    model = PPO(
        "MultiInputPolicy",
        env,
        verbose=1,
        tensorboard_log="./logs/"
    )

    model.learn(total_timesteps=1_000_000)
    model.save("models/ppo_marl")

    env.close()

if __name__ == "__main__":
    train()
```

### Running Training on Remote GPU Machine

```bash
# From the AI assistant's machine, SSH to target:
ssh target-device
cd /path/to/project

# Activate venv (uv-managed):
uv run python train_sb3.py

# Or run in background with monitoring:
tmux new-session -d -s train 'uv run python train_sb3.py'

# Monitor with tensorboard:
tensorboard --logdir ./logs/ --port 6006
# Then SSH-forward the tensorboard port:
# ssh -L 6006:127.0.0.1:6006 target-device
```

---

## Multi-Agent Patterns

### Pattern 1: Homogeneous Agents (Shared Policy)

Multiple agents share the same policy, each with its own observation/reward stream:

```
            ┌────────────────┐
            │  Shared Policy  │
            │     (PPO)       │
            └───┬────┬────┬───┘
                │    │    │
        ┌───────▼┐ ┌──▼──┐ ┌▼───────┐
        │Agent 1 │ │Ag.2│ │Agent 3 │
        │Obs→Act │ │... │ │Obs→Act │
        └────────┘ └────┘ └────────┘
```

- Use `n_agents` parameter in SyncNode
- Each agent gets its own observation/reward channel
- All agents share the same neural network weights

### Pattern 2: Heterogeneous Agents (Separate Policies)

Different agent types have different observation/action spaces:

```
┌───────────────┐  ┌───────────────┐
│  Striker PPO  │  │  Goalie PPO   │
│  (continuous) │  │  (discrete)   │
└───────┬───────┘  └───────┬───────┘
        ▼                  ▼
   ┌────────┐         ┌────────┐
   │Striker │         │ Goaler │
   │Agent   │         │ Agent  │
   └────────┘         └────────┘
```

- Requires custom environment logic to split observations
- Train separate model instances for each agent type

### Pattern 3: Self-Play

The agent plays against copies of itself:

```
Training Loop:
  1. Copy current policy → opponent
  2. Agent vs Opponent for N episodes
  3. Update policy based on results
  4. Periodically update opponent with current policy
```

---

## ONNX Export & Deployment

### Export

```bash
python train_sb3.py --onnx_export_path=GameModel.onnx
```

### Deploy in Godot

1. Use the **Godot .NET (Mono) version** of the editor
2. Place the `.onnx` file in your project
3. Configure the SyncNode to load the ONNX model path
4. The game runs inference using the trained model, no Python needed

---

## Performance Tips

| Technique | Impact |
|:----------|:-------|
| Headless mode (`show_window=false`) | 2-5x speedup |
| Use Vector observations over images | 10-100x smaller observation space |
| Parallel environments (SB3 `n_envs`) | Linear speedup up to GPU saturation |
| SampleFactory backend | Higher throughput than SB3 |
| Godot physics FPS reduction (60→30) | 2x env step speedup |

---

## Common Pitfalls

### RL Agents Plugin

- **C# project required** — the plugin is a .NET project. Must use Godot .NET version
- **Plugin activation** — must be enabled in Project Settings → Plugins after installation
- **SyncNode** — the sync node name in the scene must match the one expected by the training script
- **Observation space mismatch** — Godot and Python must agree on observation dimensions and types

### Training

- **Godot export needed** — `--env_path` requires an exported binary, or use `None` for editor mode
- **Editor mode** — Godot editor must be open and project loaded for in-editor training
- **Periodic freezing** — Normal during SB3 training when the model is updating; not a bug
- **Memory growth** — Long training runs may accumulate memory; monitor with `game_performance()`

### Remote Training

- **SSH tunnel required** — Runtime MCP tools need the TCP interaction server port forwarded
- **Latency** — Each MCP call goes through SSH; batch operations where possible
- **TensorBoard** — Forward port 6006 for local monitoring
