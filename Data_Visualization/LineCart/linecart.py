import gymnasium as gym
import torch
import torch.nn as nn
import torch.optim as optim

# Define the RL environment
env = gym.make('CartPole-v1')

# Define the RL model
class DQN(nn.Module):
    def __init__(self, n_observations, n_actions):
        super(DQN, self).__init__()
        self.layer1 = nn.Linear(n_observations, 128)
        self.layer2 = nn.Linear(128, 128)
        self.layer3 = nn.Linear(128, n_actions)

    def forward(self, x):
        x = torch.relu(self.layer1(x))
        x = torch.relu(self.layer2(x))
        return self.layer3(x)

# Train the RL model
model = DQN(env.observation_space.shape[0], env.action_space.n)
optimizer = optim.AdamW(model.parameters(), lr=0.001)

# Track rewards over episodes
rewards = []
for episode in range(100):
    state, _ = env.reset()
    episode_reward = 0
    done = False
    while not done:
        action = model(torch.tensor(state)).argmax().item()
        state, reward, done, _, _ = env.step(action)
        episode_reward += reward
    rewards.append(episode_reward)

# Plot rewards over episodes
plt.figure(figsize=(8, 6))
plt.plot(rewards)
plt.xlabel('Episode')
plt.ylabel('Reward')
plt.title('RL Agent Progress')
plt.show()