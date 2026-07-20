"""
Minimal SB3 training script for Godot RL Agents.

Usage:
    uv run python train_sb3.py [--env_path path/to/game.x86_64]

If --env_path is omitted, Godot editor mode is used
(the editor must be open with the project loaded).
"""

import argparse
from godot_rl.core.godot_env import GodotEnv
from stable_baselines3 import PPO
from stable_baselines3.common.callbacks import EvalCallback
from stable_baselines3.common.monitor import Monitor


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Train MARL agents with SB3")
    parser.add_argument(
        "--env_path", type=str, default=None,
        help="Path to exported Godot executable. Omit for editor mode."
    )
    parser.add_argument(
        "--total_timesteps", type=int, default=1_000_000,
        help="Total training timesteps"
    )
    parser.add_argument(
        "--seed", type=int, default=42, help="Random seed"
    )
    parser.add_argument(
        "--viz", action="store_true",
        help="Show Godot window during training"
    )
    parser.add_argument(
        "--onnx_export_path", type=str, default=None,
        help="Export trained model as ONNX (requires Godot .NET)"
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    # Create environment
    env = GodotEnv(
        env_path=args.env_path,
        seed=args.seed,
        show_window=args.viz,
    )

    # Wrap for SB3 monitoring
    env = Monitor(env)

    # Define policy — adjust based on observation space
    model = PPO(
        "MultiInputPolicy",
        env,
        verbose=1,
        tensorboard_log="./logs/",
        seed=args.seed,
    )

    # Evaluation callback
    eval_callback = EvalCallback(
        env,
        best_model_save_path="./models/best/",
        log_path="./logs/eval/",
        eval_freq=10_000,
        n_eval_episodes=5,
        deterministic=True,
    )

    # Train
    model.learn(
        total_timesteps=args.total_timesteps,
        callback=eval_callback,
    )

    # Save final model
    model.save("./models/ppo_marl_final")
    print(f"✅ Model saved to ./models/ppo_marl_final")

    # Export ONNX if requested
    if args.onnx_export_path:
        from sb3_onnx import export_sb3_to_onnx
        export_sb3_to_onnx(model, args.onnx_export_path)
        print(f"✅ ONNX model exported to {args.onnx_export_path}")

    env.close()


if __name__ == "__main__":
    main()
