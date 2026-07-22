"""
SampleFactory Training Config — Godot RL Agents

SampleFactory is a high-throughput RL framework for fast training.
This config connects SampleFactory to a Godot RL Agents environment.

Usage:
    # Editor mode (Godot editor running with project open):
    python samplefactory-template.py train --env-path=None
    # Or:
    sf_run.py --algo=APPO --env=godot_rl --experiment=godot_test

    # Headless binary mode:
    python samplefactory-template.py train \\
        --env-path=/path/to/game.x86_64

    # Override specific config (terminal):
    --batch_size=2048 --num_epochs=2 --lr=2e-4
"""

import argparse
import os
import sys
from typing import Optional

from godot_rl.wrappers.sample_factory_wrapper import GodotEnv

# SampleFactory imports
from sample_factory.cfg.arguments import parse_full_cfg, parse_sf_args
from sample_factory.enjoy import enjoy
from sample_factory.train import train
from sample_factory.utils.utils import strtobool


# ── Custom Godot Env Registration ───────────────────────────────
def register_custom_env(env_path: Optional[str] = None,
                        show_window: bool = False,
                        seed: int = 42,
                        n_parallel: int = 1) -> str:
    """
    Register a Godot RL Agents env with SampleFactory.

    Returns the registered env name (used by sf_experiment).
    """
    from sample_factory.envs.env_registry import register_env

    env_name = "godot_rl"

    def make_env_fn(full_env_name, cfg=None, env_config=None):
        return GodotEnv(
            env_path=env_path,
            seed=seed,
            show_window=show_window,
            n_parallel=n_parallel,
            # SampleFactory handles batching internally
            num_envs=n_parallel,
            render_mode="rgb_array" if show_window else None,
        )

    register_env(env_name, make_env_fn)
    return env_name


# ── CLI ──────────────────────────────────────────────────────────
def parse_args():
    parser = argparse.ArgumentParser()

    # Godot-specific
    parser.add_argument("--env-path", type=str, default=None,
                        help="Path to Godot exported binary. None = editor mode")
    parser.add_argument("--show-window", type=lambda x: bool(strtobool(x)),
                        default=False, nargs="?", const=True)
    parser.add_argument("--seed", type=int, default=42)

    # Action
    parser.add_argument("--mode", type=str, default="train",
                        choices=["train", "enjoy"])

    return parser.parse_args()


# ── Main ─────────────────────────────────────────────────────────
def main():
    args = parse_args()

    # 1. Register the Godot env
    env_name = register_custom_env(
        env_path=args.env_path,
        show_window=args.show_window,
        seed=args.seed,
    )

    # 2. SampleFactory config
    #    Pass --env as the registered name, --algo as APPO
    sf_args = [
        f"--env={env_name}",
        "--algo=APPO",              # SampleFactory's async PPO variant
        f"--experiment=godot_sf_{args.seed}",
        "--train_dir=./models/sample_factory",

        # === Training hyperparameters ===
        "--batch_size=2048",
        "--num_epochs=2",
        "--rollout=64",
        "--recurrence=32",
        "--hidden_size=256",
        "--lr=2.5e-4",
        "--ppo_clip_ratio=0.2",
        "--ppo_clip_value=0.2",
        "--exploration_loss_coeff=0.01",
        "--value_loss_coeff=0.5",
        "--max_grad_norm=0.5",

        # === Performance ===
        "--num_workers=8",
        "--num_envs_per_worker=2",
        "--worker_num_splits=2",
        "--batched_sampling=True",
        "--serial_mode=False",       # parallel training

        # === Reward shaping ===
        "--discount=0.99",
        "--gae_lambda=0.95",
        "--normalize_returns=True",

        # === Logging ===
        "--with_wandb=False",
        "--tensorboard=True",
        "--save_every_sec=120",
        "--keep_checkpoints=5",

        # === Evaluation ===
        "--eval_every=25",
        "--num_episodes_to_evaluate=10",
    ]

    if args.mode == "train":
        cfg = parse_full_cfg(sf_args)
        print(f"Starting SampleFactory training: env={env_name}, algo=APPO")
        train(cfg)

    elif args.mode == "enjoy":
        # Load and run a trained model
        sf_args.append("--no_render=False")
        cfg = parse_full_cfg(sf_args)
        enjoy(cfg)


if __name__ == "__main__":
    main()
