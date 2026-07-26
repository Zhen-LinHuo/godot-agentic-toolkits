# Development Workflow

## Daily Loop

```
1. Code:    Write C# script → write_file → SSH dotnet build → fix → repeat
2. Scene:   MCP tools to create scene → add nodes → configure properties
3. Verify:  Short training run to test RL integration
4. Commit:  git commit (Conventional Commits) → push feature branch
5. PR:      Open PR → review → squash merge → develop
```

## Training Pipeline

```python
# 1. Start Godot as subprocess (via godot-rl)
# 2. Configure training parameters (hyperparams.yaml)
# 3. Run training (SB3/CleanRL/SampleFactory)
# 4. Monitor with TensorBoard
# 5. Export model to ONNX
# 6. Import ONNX into Godot project
```

See template files in `templates/training/`:
- `sb3_ppo.py` — PPO training with StableBaselines3
- (CleanRL and SampleFactory templates coming soon)

## Git Workflow

```
main        ← PR merges only (stable releases)
develop     ← active development (free push)
feat/*      ← features (PR → develop)
fix/*       ← bug fixes (PR → develop)
```

## Remote Device Operations

| Operation | Method |
|:----------|:-------|
| Code edit | write_file → SSH dotnet build |
| Scene ops | MCP tools over SSH tunnel |
| Training | SSH → python train.py |
| Monitoring | SSH tunnel → TensorBoard |
| Model deploy | scp from training → dev machine |
