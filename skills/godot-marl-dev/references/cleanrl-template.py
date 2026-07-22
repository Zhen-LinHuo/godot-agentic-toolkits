"""
CleanRL PPO Training Template — Godot RL Agents

Single-file PPO implementation that connects to a Godot environment.
Based on CleanRL's ppo_continuous_action.py.

Usage:
    uv run python cleanrl-template.py                          # editor mode
    uv run python cleanrl-template.py --env-path game.x86_64   # headless binary
"""

# ── Imports ──────────────────────────────────────────────────────
import argparse
import os
import random
import time
from collections import deque
from dataclasses import dataclass
from distutils.util import strtobool
from typing import Optional

import gymnasium as gym
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from torch.distributions.categorical import Categorical
from torch.distributions.normal import Normal
from torch.utils.tensorboard import SummaryWriter

# Godot RL Agents wrapper
from godot_rl.wrappers.cleanrl_wrapper import CleanRLGodotEnv


# ── CLI ──────────────────────────────────────────────────────────
def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--exp-name", type=str, default="godot_cleanrl")
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--torch-deterministic", type=lambda x: bool(strtobool(x)), default=True, nargs="?", const=True)

    # Godot env
    parser.add_argument("--env-path", type=str, default=None, help="Path to exported Godot binary. None = editor mode")
    parser.add_argument("--n-envs", type=int, default=1)
    parser.add_argument("--show-window", type=lambda x: bool(strtobool(x)), default=False, nargs="?", const=True)

    # PPO hyperparams
    parser.add_argument("--total-timesteps", type=int, default=1_000_000)
    parser.add_argument("--learning-rate", type=float, default=2.5e-4)
    parser.add_argument("--num-steps", type=int, default=128)
    parser.add_argument("--gamma", type=float, default=0.99)
    parser.add_argument("--gae-lambda", type=float, default=0.95)
    parser.add_argument("--update-epochs", type=int, default=4)
    parser.add_argument("--clip-coef", type=float, default=0.2)
    parser.add_argument("--ent-coef", type=float, default=0.01)
    parser.add_argument("--vf-coef", type=float, default=0.5)
    parser.add_argument("--max-grad-norm", type=float, default=0.5)
    parser.add_argument("--batch-size", type=int, default=64)
    parser.add_argument("--minibatch-size", type=int, default=32)

    # Logging
    parser.add_argument("--track", type=lambda x: bool(strtobool(x)), default=True, nargs="?", const=True)
    parser.add_argument("--log-dir", type=str, default="./logs/cleanrl")

    return parser.parse_args()


# ── Network ──────────────────────────────────────────────────────
class Agent(nn.Module):
    """PPO Actor-Critic network."""

    def __init__(self, observation_space, action_space):
        super().__init__()
        self.obs_dim = observation_space.shape[0]

        if isinstance(action_space, gym.spaces.Discrete):
            self.action_dim = action_space.n
            self.is_discrete = True
        elif isinstance(action_space, gym.spaces.Box):
            self.action_dim = action_space.shape[0]
            self.is_discrete = False
        else:
            raise ValueError(f"Unsupported action space: {action_space}")

        # Shared feature extractor
        self.features = nn.Sequential(
            nn.Linear(self.obs_dim, 64),
            nn.Tanh(),
            nn.Linear(64, 64),
            nn.Tanh(),
        )

        # Policy head
        if self.is_discrete:
            self.actor = nn.Linear(64, self.action_dim)
        else:
            self.actor_mean = nn.Linear(64, self.action_dim)
            self.actor_logstd = nn.Parameter(torch.zeros(1, self.action_dim))

        # Value head
        self.critic = nn.Linear(64, 1)

    def get_value(self, x):
        return self.critic(self.features(x))

    def get_action_and_value(self, x, action=None):
        features = self.features(x)
        value = self.critic(features)

        if self.is_discrete:
            logits = self.actor(features)
            probs = Categorical(logits=logits)
            if action is None:
                action = probs.sample()
            return action, probs.log_prob(action), probs.entropy(), value

        mean = self.actor_mean(features)
        std = self.actor_logstd.exp().expand_as(mean)
        probs = Normal(mean, std)
        if action is None:
            action = probs.sample()
        return action, probs.log_prob(action).sum(-1), probs.entropy().sum(-1), value


# ── Rollout Buffer ───────────────────────────────────────────────
@dataclass
class Storage:
    obs: torch.Tensor
    actions: torch.Tensor
    logprobs: torch.Tensor
    rewards: torch.Tensor
    dones: torch.Tensor
    values: torch.Tensor


# ── Training Loop ────────────────────────────────────────────────
def train():
    args = parse_args()
    run_name = f"{args.exp_name}__{int(time.time())}"
    writer = SummaryWriter(f"{args.log_dir}/{run_name}")
    writer.add_text("hyperparameters", str(vars(args)))

    # Seeding
    random.seed(args.seed)
    np.random.seed(args.seed)
    torch.manual_seed(args.seed)
    if args.torch_deterministic:
        torch.backends.cudnn.deterministic = True
        torch.backends.cudnn.benchmark = False

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Device: {device}")

    # Environment
    env = CleanRLGodotEnv(
        env_path=args.env_path,
        seed=args.seed,
        show_window=args.show_window,
        n_parallel=args.n_envs,
    )
    assert isinstance(env.action_space, (gym.spaces.Discrete, gym.spaces.Box)), \
        "Only Discrete and Box action spaces supported"

    # Agent
    agent = Agent(env.observation_space, env.action_space).to(device)
    optimizer = optim.Adam(agent.parameters(), lr=args.learning_rate, eps=1e-5)

    # Storage
    obs = torch.zeros((args.num_steps, args.n_envs) + env.observation_space.shape).to(device)
    actions = torch.zeros((args.num_steps, args.n_envs) + env.action_space.shape
                          if isinstance(env.action_space, gym.spaces.Box)
                          else (args.num_steps, args.n_envs)).to(device)
    logprobs = torch.zeros((args.num_steps, args.n_envs)).to(device)
    rewards = torch.zeros((args.num_steps, args.n_envs)).to(device)
    dones = torch.zeros((args.num_steps, args.n_envs)).to(device)
    values = torch.zeros((args.num_steps, args.n_envs)).to(device)

    # Training
    global_step = 0
    next_obs, _ = env.reset()
    next_obs = torch.Tensor(next_obs).to(device)
    next_done = torch.zeros(args.n_envs).to(device)
    num_updates = args.total_timesteps // args.num_steps // args.n_envs

    print(f"Starting CleanRL PPO: {args.total_timesteps} steps in {num_updates} updates")

    for update in range(1, num_updates + 1):
        start_time = time.time()

        # ── Collect rollout ──
        for step in range(args.num_steps):
            global_step += args.n_envs
            obs[step] = next_obs
            dones[step] = next_done

            with torch.no_grad():
                action, logprob, _, value = agent.get_action_and_value(next_obs)
                values[step] = value.flatten()

            actions[step] = action
            logprobs[step] = logprob

            # Step env
            next_obs, reward, terminations, truncations, infos = env.step(
                action.cpu().numpy())
            next_done = np.logical_or(terminations, truncations)
            rewards[step] = torch.Tensor(reward).to(device).view(-1)
            next_obs = torch.Tensor(next_obs).to(device)
            next_done = torch.Tensor(next_done).to(device)

            # Log episodic returns
            if "episode" in infos and "r" in infos["episode"]:
                for i, ep_return in enumerate(infos["episode"]["r"]):
                    if ep_return is not None:
                        writer.add_scalar("charts/episodic_return", ep_return, global_step)

        # ── GAE + returns ──
        with torch.no_grad():
            next_value = agent.get_value(next_obs).reshape(1, -1)
            advantages = torch.zeros_like(rewards).to(device)
            last_gae = 0
            for t in reversed(range(args.num_steps)):
                if t == args.num_steps - 1:
                    next_non_terminal = 1.0 - next_done
                    next_values = next_value
                else:
                    next_non_terminal = 1.0 - dones[t + 1]
                    next_values = values[t + 1]
                delta = rewards[t] + args.gamma * next_values * next_non_terminal - values[t]
                last_gae = delta + args.gamma * args.gae_lambda * next_non_terminal * last_gae
                advantages[t] = last_gae
            returns = advantages + values

        # ── Optimisation ──
        b_obs = obs.reshape((-1,) + env.observation_space.shape)
        b_actions = actions.reshape((-1,) + (actions.shape[-1],)
                                     if isinstance(env.action_space, gym.spaces.Box)
                                     else (-1,))
        b_logprobs = logprobs.reshape(-1)
        b_advantages = advantages.reshape(-1)
        b_returns = returns.reshape(-1)
        b_values = values.reshape(-1)

        b_inds = np.arange(args.batch_size)
        clipfracs = []

        for epoch in range(args.update_epochs):
            np.random.shuffle(b_inds)
            for start in range(0, args.batch_size, args.minibatch_size):
                end = start + args.minibatch_size
                mb_inds = b_inds[start:end]

                _, new_logprob, entropy, new_value = agent.get_action_and_value(
                    b_obs[mb_inds], b_actions.long()[mb_inds]
                    if isinstance(env.action_space, gym.spaces.Discrete)
                    else b_actions[mb_inds])
                logratio = new_logprob - b_logprobs[mb_inds]
                ratio = logratio.exp()

                with torch.no_grad():
                    approx_kl = ((ratio - 1) - logratio).mean()
                    clipfracs += [((ratio - 1).abs() > args.clip_coef).float().mean().item()]

                mb_advantages = b_advantages[mb_inds]
                mb_advantages = (mb_advantages - mb_advantages.mean()) / (mb_advantages.std() + 1e-8)

                # Policy loss
                pg_loss1 = -mb_advantages * ratio
                pg_loss2 = -mb_advantages * torch.clamp(ratio, 1 - args.clip_coef, 1 + args.clip_coef)
                pg_loss = torch.max(pg_loss1, pg_loss2).mean()

                # Value loss
                new_value = new_value.view(-1)
                v_loss = 0.5 * ((new_value - b_returns[mb_inds]) ** 2).mean()

                # Entropy bonus
                entropy_loss = entropy.mean()

                loss = pg_loss - args.ent_coef * entropy_loss + v_loss * args.vf_coef

                optimizer.zero_grad()
                loss.backward()
                nn.utils.clip_grad_norm_(agent.parameters(), args.max_grad_norm)
                optimizer.step()

        # ── Logging ──
        y_pred, y_true = b_values.cpu().numpy(), b_returns.cpu().numpy()
        var_y = np.var(y_true)
        explained_var = np.nan if var_y == 0 else 1 - np.var(y_true - y_pred) / var_y

        writer.add_scalar("charts/learning_rate", optimizer.param_groups[0]["lr"], global_step)
        writer.add_scalar("losses/value_loss", v_loss.item(), global_step)
        writer.add_scalar("losses/policy_loss", pg_loss.item(), global_step)
        writer.add_scalar("losses/entropy", entropy_loss.item(), global_step)
        writer.add_scalar("losses/approx_kl", approx_kl.item(), global_step)
        writer.add_scalar("losses/clipfrac", np.mean(clipfracs), global_step)
        writer.add_scalar("losses/explained_variance", explained_var, global_step)
        writer.add_scalar("charts/sps", int(global_step / (time.time() - start_time)), global_step)

        if update % 10 == 0:
            print(f"  Update {update}/{num_updates}: "
                  f"global_step={global_step}, "
                  f"episodic_return={infos.get('episode', {}).get('r', [[0]])[-1][0]:.2f}")

    # ── Save ──
    model_path = f"models/cleanrl_ppo_{run_name}.pt"
    os.makedirs("models", exist_ok=True)
    torch.save(agent.state_dict(), model_path)
    print(f"Model saved to {model_path}")

    # ── Export to ONNX ──
    agent.eval()
    dummy_obs = torch.randn(1, env.observation_space.shape[0])
    onnx_path = f"models/cleanrl_ppo_{run_name}.onnx"
    torch.onnx.export(
        agent,
        dummy_obs,
        onnx_path,
        input_names=["observation"],
        output_names=["action", "value"],
        opset_version=17,
        dynamo=False,
    )
    print(f"ONNX exported to {onnx_path}")

    env.close()
    writer.close()
    print("✅ CleanRL training complete")


if __name__ == "__main__":
    train()
