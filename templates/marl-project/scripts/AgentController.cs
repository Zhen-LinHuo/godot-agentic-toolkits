using Godot;
using System;

namespace MarlProject
{
    /// <summary>
    /// Base controller for MARL agents.
    /// Each agent uses the Godot RL Agents SyncNode to communicate
    /// observations, actions, and rewards with the training pipeline.
    /// </summary>
    public partial class AgentController : CharacterBody2D
    {
        [Export]
        public int AgentId { get; set; }

        [Export]
        public float MoveSpeed { get; set; } = 200.0f;

        // Called by SyncNode each step — override in subclass
        public virtual float[] GetObservation()
        {
            return Array.Empty<float>();
        }

        // Called by SyncNode to apply an action from the policy
        public virtual void ApplyAction(float[] action)
        {
            // Default: continuous movement (action[0]=x, action[1]=y)
            if (action.Length >= 2)
            {
                Velocity = new Vector2(action[0], action[1]) * MoveSpeed;
                MoveAndSlide();
            }
        }

        // Called by SyncNode to calculate reward for this step
        public virtual float CalculateReward()
        {
            return 0.0f;
        }

        // Called when episode resets
        public virtual void OnEpisodeBegin()
        {
            // Reset agent state for new episode
        }
    }
}
