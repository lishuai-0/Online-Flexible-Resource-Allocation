"""Initial training of the agents using the basic environments"""

from __future__ import annotations

from agents.rl_agents.agents.ddpg import ResourceWeightingSeq2SeqAgent
from agents.rl_agents.agents.dqn import TaskPricingDqnAgent
from agents.rl_agents.neural_networks.ddpg_networks import create_seq2seq_actor_network, create_seq2seq_critic_network
from agents.rl_agents.neural_networks.dqn_networks import create_lstm_dqn_network
from env.environment import OnlineFlexibleResourceAllocationEnv
from training.train_agents import generate_eval_envs, run_training, setup_tensorboard

if __name__ == "__main__":
    folder = 'seq2seq_resource_weighting'
    writer, datetime = setup_tensorboard('training/results/logs/', folder)

    save_folder = f'{folder}_{datetime}'

    env = OnlineFlexibleResourceAllocationEnv([
        './training/settings/basic.env',
        './training/settings/large_tasks_servers.env',
        './training/settings/limited_resources.env',
        './training/settings/mixture_tasks_servers.env'
    ])
    eval_envs = generate_eval_envs(env, 20, f'./training/settings/eval_envs/network_arch/')

    task_pricing_agents = [
        TaskPricingDqnAgent(agent_num, create_lstm_dqn_network(9, 21), save_folder=save_folder)
        for agent_num in range(3)
    ]
    resource_weighting_agents = [
        ResourceWeightingSeq2SeqAgent(0, create_seq2seq_actor_network(), create_seq2seq_critic_network(),
                                      create_seq2seq_critic_network(), save_folder=save_folder)
    ]

    with writer.as_default():
        run_training(env, eval_envs, 600, task_pricing_agents, resource_weighting_agents, 10)

    for agent in task_pricing_agents:
        agent.save()
    for agent in resource_weighting_agents:
        agent.save()
