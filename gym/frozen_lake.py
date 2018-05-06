import time
import random
import gym
from gym.envs.registration import register
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt


register(
    id='FrozenLake-v3',
    entry_point='gym.envs.toy_text:FrozenLakeEnv',
    kwargs={
        'map_name': '4x4',
        'is_slippery': False,
    }
)
env = gym.make('FrozenLake-v3')


# Argmax that chooses randomly among eligible maximum indices.
def random_argmax(vector):
    m = np.amax(vector)
    indices = np.nonzero(vector == m)[0]
    return random.choice(indices)


Q = np.zeros([env.observation_space.n, env.action_space.n])
num_episodes = 2000

reward_list = list()
for i in range(num_episodes):
    state = env.reset()
    reward_all = 0
    done = False

    while not done:
        action = random_argmax(Q[state, :])

        new_state, reward, done, info = env.step(action)
            
        Q[state, action] = reward + np.max(Q[new_state, :])

        state = new_state
        reward_all += reward
    
    reward_list.append(reward_all)

print('Success rate:', sum(reward_list)/num_episodes)
print('Final Q-Table Vlaues')
print('left down right up')
print(Q)

plt.bar(range(len(reward_list)), reward_list)
plt.show()
