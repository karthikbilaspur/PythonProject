import gym
import numpy as np
import random
import matplotlib.pyplot as plt

# Environment setup
env = gym.make('FrozenLake-v1')

# Q-table creation
action_size = env.action_space.n
state_size = env.observation_space.n
q_table = np.zeros((state_size, action_size))

# Q-learning parameters
learning_rate = 0.85
discount_rate = 0.98
exploration_rate = 1
max_exploration_rate = 1
min_exploration_rate = 0.01
exploration_decay_rate = 0.01
num_episodes = 10000
max_steps_per_episode = 100

# Q-learning algorithm
rewards_all_episodes = []
for episode in range(num_episodes):
    state = env.reset()
    done = False
    rewards_current_episode = 0

    for step in range(max_steps_per_episode):
        exploration_threshold = random.uniform(0, 1)
        if exploration_threshold > exploration_rate:
            action = np.argmax(q_table[state, :])
        else:
            action = env.action_space.sample()

        new_state, reward, done, info = env.step(action)

        q_table[state, action] = q_table[state, action] * (1 - learning_rate) + learning_rate * (
            reward + discount_rate * np.max(q_table[new_state, :]))

        state = new_state
        rewards_current_episode += reward

        if done:
            break

    exploration_rate = min_exploration_rate + \
        (max_exploration_rate - min_exploration_rate) * np.exp(-exploration_decay_rate * episode)
    rewards_all_episodes.append(rewards_current_episode)

# Calculate and print average reward per thousand episodes
rewards_per_thousand_episodes = np.split(np.array(rewards_all_episodes), num_episodes / 1000)
count = 1000
for r in rewards_per_thousand_episodes:
    print(count, ":", str(sum(r / 1000)))
    count += 1000

# Visualize agent
for episode in range(3):
    state = env.reset()
    done = False
    print("Episode:", episode)
    for step in range(max_steps_per_episode):
        env.render()
        action = np.argmax(q_table[state, :])
        new_state, reward, done, info = env.step(action)
        state = new_state
        if done:
            env.render()
            if reward == 1:
                print("Goal reached!")
            else:
                print("Failed to reach goal")
            break
env.close()

# Plot rewards
plt.plot(rewards_all_episodes)
plt.xlabel('Episode')
plt.ylabel('Reward')
plt.title('Rewards over Episodes')
plt.show()

# Plot smoothed rewards
smoothed_rewards = [np.mean(rewards_all_episodes[max(0, i-100):i+1]) for i in range(len(rewards_all_episodes))]
plt.plot(smoothed_rewards)
plt.xlabel('Episode')
plt.ylabel('Smoothed Reward')
plt.title('Smoothed Rewards over Episodes')
plt.show()