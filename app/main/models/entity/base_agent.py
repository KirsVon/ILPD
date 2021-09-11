#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : fengchong
# @Time    : 2020/12/13
# @File    : base_agent.py
import numpy as np
import pandas as pd
import gym
import random
import math
import sys


class BaseAgent(object):
    def __init__(self, action_space: [], gama=0.6, learning_rate=0.5, lmin=1, lmax=11):
        # self.batch = test_batch()
        self.actions = action_space  # 动作空间
        self.state = (0, 0, 0)
        self.reward = 0
        self.done = False
        self.lmin = lmin
        self.gama = gama
        self.lmax = lmax
        self.lr = learning_rate
        self.q_table = [[[[random.random() for i in range(lmax)] for i in range(lmax)] for i in range(300)] for i in range(30)]
        for i in range(30):  # i = Nl
            for j in range(300):  # j = Nr
                for k in range(lmax):  # k = l
                    for l in range(k):  # l = lp
                        self.q_table[i][j][k][l] = 0  # lp < l Q表值为0          初始化Q表

    def update_q_table(self, state: tuple, action: int, reward: int, next_state: tuple):  # 更新Q表
        assert action in self.actions, print(action)
        try:
            if reward != 0:
                self.q_table[state[0]][state[1]][state[2]][action] = \
                self.q_table[state[0]][state[1]][state[2]][action] + self.lr * (
                            reward + self.gama * max(self.q_table[next_state[0]][next_state[1]][next_state[2]]) -
                            self.q_table[state[0]][state[1]][state[2]][action])
            else:
                self.q_table[state[0]][state[1]][state[2]][action] = \
                self.q_table[state[0]][state[1]][state[2]][action] + self.lr * (
                        self.gama * max(self.q_table[next_state[0]][next_state[1]][next_state[2]]) -
                            self.q_table[state[0]][state[1]][state[2]][action])
        except IndexError:
            print(state)
            print(next_state)
    def get_next_action(self, state: tuple):
        try:
            lp = np.argmax(self.q_table[state[0]][state[1]][state[2]])
            return lp
        except IndexError:
            print(state)

    def load_Q_table(self, filepath: str):  # 学习生成的Q表放在csv中，待需要时拿来直接用
        df = pd.read_csv(filepath)
        q_value = list(df["Q_value"])
        count = 0
        # for i in range(self.lmax):  # i = Nl
        #     for j in range(self.lmax):  # j = Nr
        #         for k in range(self.lmax - self.lmin):  # k = l
        #             for l in range(self.lmax - self.lmin):  # l = lp
        #                 self.q_table[i][j][k][l] = q_value[count]
        #                 count += 1
        for i in range(30):  # i = Nl
            for j in range(300):  # j = Nr
                for k in range(self.lmax):  # k = l
                    for l in range(self.lmax):  # l = lp
                        self.q_table[i][j][k][l] = q_value[count]
                        count += 1

    def save_q_table(self,date:str):
        q_list = []
        for i in range(30):  # i = Nl
            for j in range(300):  # j = Nr
                for k in range(self.lmax):  # k = l
                    for l in range(self.lmax):
                        q_list.append(self.q_table[i][j][k][l])
        df = pd.DataFrame(columns=['Q_value'])
        df['Q_value'] = q_list
        df.to_csv('/./data/FC/experiment/0908/' + date + '.csv')
