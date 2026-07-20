using Godot;
using System;
using System.Collections.Generic;

namespace MarlProject
{
    /// <summary>
    /// Central training manager — coordinates the Godot RL Agents SyncNode,
    /// manages agents, and provides episode lifecycle hooks.
    /// </summary>
    public partial class TrainingManager : Node2D
    {
        [Export]
        public PackedScene AgentScene { get; set; }

        [Export]
        public int AgentCount { get; set; } = 4;

        private readonly List<AgentController> _agents = new();

        public override void _Ready()
        {
            SpawnAgents();
        }

        private void SpawnAgents()
        {
            if (AgentScene == null)
                return;

            for (int i = 0; i < AgentCount; i++)
            {
                var agent = AgentScene.Instantiate<AgentController>();
                agent.AgentId = i;
                agent.Position = new Vector2(
                    GD.RandRange(-200, 200),
                    GD.RandRange(-200, 200)
                );
                AddChild(agent);
                _agents.Add(agent);
            }
        }

        public void OnEpisodeBegin()
        {
            foreach (var agent in _agents)
            {
                agent.OnEpisodeBegin();
            }
        }
    }
}
