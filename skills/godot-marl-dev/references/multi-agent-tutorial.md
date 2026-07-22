# Multi-Agent Tutorial: Godot RL Agents

> Step-by-step guide to building multi-agent environments in Godot,
> from a simple homogeneous setup to self-play.
> Assumes Godot 4.4+ with RL Agents plugin installed.

---

## 1. Understanding Multi-Agent in Godot RL Agents

Godot RL Agents supports multiple agents through the `Sync` node. Each agent
gets its own observation/reward stream, but all agents communicate through
the same Sync node to the Python training script.

There are two fundamental setups:

| Setup | Policy | Observation Space | Action Space | Use Case |
|-------|--------|-------------------|--------------|----------|
| **Homogeneous** | Shared | Same shape | Same shape | Symmetric teams (robots, enemies) |
| **Heterogeneous** | Separate | Different shapes | Different shapes | Asymmetric roles (striker vs goalie) |
| **Self-Play** | Shared + opponent copy | Same shape | Same shape | Competitive learning |

---

## 2. Homogeneous Agents (Shared Policy)

Multiple identical agents share one policy network. Best for symmetric scenarios
like swarm robotics, team sports, or cooperative tasks.

### Godot Setup

1. Create a scene with multiple agent nodes:

```
Main (Node)
├── Sync (Sync node from RL Agents plugin) — n_agents=4
├── Agent1 (CharacterBody2D)
│   ├── Sprite
│   └── CollisionShape
├── Agent2 (CharacterBody2D) — same structure
├── Agent3 (CharacterBody2D) — same structure
└── Agent4 (CharacterBody2D) — same structure
```

2. Configure the Sync node:
   - **n_agents**: 4 (number of agents)
   - **observation_space**: Vector (e.g., 10 floats per agent)
   - **action_space**: Discrete (e.g., 5 actions per agent)
   - **agent_reward_section**: Checked (each agent gets individual rewards)

3. Attach a script to each agent that sends observations and receives actions:

```csharp
// AgentController.cs — homogeneous agent script
using Godot;
using System.Linq;

public partial class AgentController : CharacterBody2D
{
    [Export]
    public int AgentId { get; set; }

    private Sync _sync;

    public override void _Ready()
    {
        _sync = GetNode<Sync>("/root/Main/Sync");
    }

    public override void _PhysicsProcess(double delta)
    {
        // Send observation to Sync node
        float[] obs = GetObservations();
        _sync.SetObservation(AgentId, obs);

        // Get action from trained policy (via Sync)
        int action = _sync.GetAction(AgentId);

        // Apply action
        ApplyAction(action);
    }

    private float[] GetObservations()
    {
        // Return agent-specific observations
        // e.g., position, velocity, nearby agents, etc.
        return new float[] {
            (float)Position.X,
            (float)Position.Y,
            // ... more observations
        };
    }

    private void ApplyAction(int action)
    {
        switch (action)
        {
            case 0: // Move up
                Velocity = new Vector2(0, -100);
                break;
            case 1: // Move down
                Velocity = new Vector2(0, 100);
                break;
            case 2: // Move left
                Velocity = new Vector2(-100, 0);
                break;
            case 3: // Move right
                Velocity = new Vector2(100, 0);
                break;
            case 4: // Stay
                Velocity = Vector2.Zero;
                break;
        }
        MoveAndSlide();
    }
}
```

### Python Training

```python
# train_homogeneous.py
from godot_rl.wrappers.stable_baselines_wrapper import StableBaselinesGodotEnv
from stable_baselines3 import PPO

# Important: n_parallel sets the number of parallel Godot instances,
# NOT the number of agents per instance.
# Number of agents per instance is set in the Sync node (n_agents=4).
env = StableBaselinesGodotEnv(
    env_path=None,
    seed=42,
    show_window=False,
    n_parallel=1,
)

# The observation space includes all agents' observations.
# PPO's MultiInputPolicy handles structured observations.
model = PPO(
    "MultiInputPolicy",
    env,
    verbose=1,
    tensorboard_log="./logs/",
    n_steps=2048,
    batch_size=64,
)

model.learn(total_timesteps=1_000_000)
model.save("models/homogeneous_ppo")
env.close()
```

---

## 3. Heterogeneous Agents (Separate Policies)

Different agent roles require different observation/action spaces.
Example: a striker (continuous movement) and a goalie (discrete actions).

### Godot Setup

Use two separate Sync nodes, one per agent type:

```
Main (Node)
├── SyncStriker (Sync) — for striker agents
│   obs_space: Vector(12), act_space: Discrete(3)
├── SyncGoalie (Sync) — for goalie agents
│   obs_space: Vector(15), act_space: Discrete(5)
├── Striker (CharacterBody2D)
└── Goalie (CharacterBody2D)
```

Each agent type has its own training script:

```python
# train_striker.py
striker_env = StableBaselinesGodotEnv(
    env_path=None,
    seed=42,
    show_window=False,
    # The env config tells Godot to only use the Striker sync node
    config={"agent_type": "striker"},
)
```

```python
# train_goalie.py
goalie_env = StableBaselinesGodotEnv(
    env_path=None,
    seed=42,
    show_window=False,
    config={"agent_type": "goalie"},
)
```

### Reward Design Tips for Heterogeneous

| Role | Reward Signal | Example |
|------|---------------|---------|
| Striker | Goal-scoring reward | +10 for goal, -0.1 per second |
| Goalie | Save reward | +5 for save, -1 for goal against |
| Both | Shaping reward | +0.1 for proximity to ball |

---

## 4. Self-Play

The agent plays against copies of itself, with periodic policy swapping.

### Game Loop

```
1. Current policy plays against an opponent (old policy copy)
2. Both agents receive rewards based on the game outcome
3. Policy is updated to maximise its reward
4. Every N episodes: copy current policy → opponent
5. Repeat
```

### Python Implementation

```python
"""Self-play training loop."""
from copy import deepcopy
import numpy as np
from godot_rl.wrappers.stable_baselines_wrapper import StableBaselinesGodotEnv
from stable_baselines3 import PPO

env = StableBaselinesGodotEnv(
    env_path=None,
    show_window=False,
    n_parallel=1,
)

model = PPO("MultiInputPolicy", env, verbose=1, n_steps=2048)
opponent = deepcopy(model.policy)  # initial opponent = current policy

UPDATE_INTERVAL = 10  # update opponent every 10 training iterations
episode = 0

for i in range(500):
    model.learn(total_timesteps=2048, reset_num_timesteps=False)

    episode += 1
    if episode % UPDATE_INTERVAL == 0:
        # Opponent becomes a snapshot of current policy
        opponent = deepcopy(model.policy)
        print(f"Opponent updated at episode {episode}")

model.save("models/selfplay_ppo")
env.close()
```

### Godot Script — Self-Play Aware

```csharp
// Agent must distinguish self from opponent
public partial class PlayerAgent : CharacterBody2D
{
    [Export]
    public bool IsOpponent { get; set; } = false;

    public override void _Ready()
    {
        if (IsOpponent)
            Modulate = Colors.Red;   // visual distinction
        else
            Modulate = Colors.Blue;
    }
}
```

---

## 5. Debugging Multi-Agent

### Common Issues

| Symptom | Likely Cause | Fix |
|---------|-------------|-----|
| All agents take the same action | Shared policy + identical observations | Add agent-specific noise or unique ID to observation |
| Training loss is flat | Agents not receiving rewards | Check `EmitSignal(SignalName.Reward)` in Godot |
| One agent dominates | Reward imbalance | Normalise rewards per agent type |
| ONNX model wrong output shape | Multi-agent flattens obs incorrectly | Check `observation_space` dimensions match |

### Verification: Agent Isolation

Run with a single agent type first to verify each component:

```bash
# Test striker in isolation (goalie disabled)
env = StableBaselinesGodotEnv(
    config={"test_mode": "striker_only"},
)

# Test goalie in isolation (striker disabled)
env = StableBaselinesGodotEnv(
    config={"test_mode": "goalie_only"},
)

# Then test both together
env = StableBaselinesGodotEnv(config={})
```

### Verified Checklist

- [ ] Each agent sends unique observations (add `agent_id` to observation vector)
- [ ] Rewards are per-agent, not global (set `agent_reward_section` in Sync node)
- [ ] Actions are correctly mapped to agent-specific behaviours
- [ ] n_agents in Sync node matches the scene's agent count
- [ ] Training script's observation/action spaces match Godot config

---

## 6. Next Steps

1. Start with homogeneous (simplest) — get one policy training
2. Move to heterogeneous — separate policies for asymmetric roles
3. Add self-play — competitive learning with policy swapping
4. Benchmark: homogeneous → heterogeneous → self-play performance
