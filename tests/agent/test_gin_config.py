"""
Tests the use of gin configurable with agent and network classes
"""

import gin

from agents.rl_agents.agents.ddpg import TaskPricingDdpgAgent
from agents.rl_agents.agents.dqn import TaskPricingDqnAgent
from agents.rl_agents.neural_networks.ddpg_networks import create_lstm_actor_network, create_lstm_critic_network
from agents.rl_agents.neural_networks.dqn_networks import create_lstm_dqn_network


def test_agent_gin():
    # Add basic gin parse config
    gin.parse_config("""
    import agents.rl_agents.rl_agents

    ReinforcementLearningAgent.save_frequency = 4
    """)

    test_agent = TaskPricingDqnAgent(0, create_lstm_dqn_network(9, 10))
    assert test_agent.save_frequency == 4


def test_standard_gin_config():
    # Try parsing the standard gin config to confirm that the file is valid
    gin.parse_config_file('../src/training/settings/standard_config.gin')

    TaskPricingDqnAgent(0, create_lstm_dqn_network(9, 10))
    TaskPricingDdpgAgent(0, create_lstm_actor_network(9), create_lstm_critic_network(9))
