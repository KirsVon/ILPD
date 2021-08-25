# -*- coding: utf-8 -*-
# Description:
# Created: liujiaye  2019/12/13

import numpy as np

from app.main.models.entity.truck_agent import TruckAgent
from app.main.models.entity.base_environment import Env
from app.main.entity.car import Car

np.random.seed(1)


class RFL:
    def __init__(self, cargo_list):
        self.cargo_list = cargo_list

    def train_one(self):
        env = Env(self.cargo_list, 60)
        agent = TruckAgent(actions=list(range(env.n_actions)))
        for episode in range(1000):
            # reset environment and initialize state
            state = env.reset()
            # get action of state from agent
            action = agent.get_action(str(state))
            while True:
                env.render()
                # take action and proceed one step in the environment
                next_state, reward, done = env.step(action)
                next_action = agent.get_action(str(next_state))
                # with sample <s,a,r,s',a'>, agent learns new q function
                agent.learn(str(state), action, reward, str(next_state), next_action)
                state = next_state
                action = next_action
                # print q function of all states at screen
                # if episode ends, then break
                if done:
                    break

    def run(self, cargo_state, car):
        pass


if __name__ == '__main__':
    cargo_list = []
    car_sample = Car([])
    sample = RFL(cargo_list, car_sample)
    sample.train()
    cargo_state = []
    sample.run(cargo_state, car_sample)
