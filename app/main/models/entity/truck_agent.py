# -*- coding: utf-8 -*-
# Description:
# Created: liujiaye  2020/03/01
import pandas as pd
from app.main.models.entity.base_agent import BaseAgent


class TruckAgent(BaseAgent):
    def __init__(self,actions):
        super(TruckAgent, self).__init__(actions)
        self.lamda = 0.9
        self.trace = self.q_table.copy()

    # with sample <s, a, r, s', a'>, learns new q function
    def learn(self, state, action, reward, next_state, next_action):
        self.check_state_exist(state)
        current_q = self.q_table.loc[state, action]
        next_state_q = self.q_table.loc[next_state, next_action]
        td_error = reward + self.discount_factor * next_state_q - current_q
        self.trace.loc[state, action] += 1
        self.q_table += self.learning_rate * td_error * self.trace
        self.trace *= self.discount_factor * self.lamda

    def check_state_exist(self, state):
        if state not in self.q_table.index:
            to_be_append = pd.Series(
                [0] * len(self.actions),
                index=self.q_table.columns,
                name=state,
            )
            self.q_table = self.q_table.append(to_be_append)
            self.trace = self.trace.append(to_be_append)
