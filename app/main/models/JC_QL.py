# -*- coding: utf-8 -*-
# @Author  : fengchong
# @Time    : 2020/12/29
# @File    : RQL.py
import datetime
from typing import List

from app.main.controller.cargo_maintain import cargo_management
from app.main.entity.batch import Batch
from app.main.entity.car import Car
from app.main.models.kuhn_munkras import kuhn_munkras
from app.main.models.entity import base_agent
import numpy as np
import pandas as pd
from  datetime import  datetime, timedelta
import random
import math
import sys
from app.main.models.entity.environment import Environment
from app.main.models.entity.base_agent import BaseAgent
from app.main.controller.config_name_management import curr_config_class

min_length = 1
max_length = 10
car_file_path = ''
test_car_file_path = ''
env = Environment(1,10,curr_config_class.CAR_DATA_ROOT_DIRECTORY + '20201009000000.csv', '20201009000000', '20201010000000', '20201014000000')


class JC_QL:

    def __init__(self, learning_rate=0.5, lmin=min_length, lmax=max_length):
        self.learning_rate = learning_rate  # Restricted Q-Learning 学习因子
        self.lmax = lmax  # 批的最大长度
        self.lmin = lmin  # 批的最小长度
        self.agent = BaseAgent(env.action_space)
        self.timestamp = 0  # 测试时所用时间戳
        self.batch = Batch()  # 测试时随用批
        self.l = 0  # 批的长度
        self.end = False  # 单一episode是否结束

    def train(self, iter_time: int,total_timestamp_len):
        t = 0  # 当前时间戳
        lt = 0  # 当前批长度
        lp = 0  # 当前批长度匹配时最佳长度
        H = total_timestamp_len  # 这一episode的长度
        rt = 0  # reward、即时奖励
        state = (0, 0, 0)  # 初始时状态 三元组 第一个位置代表左边节点数，第二个位置代表右边节点数，第三个位置代表当前批的长度
        done = False  # 这一episode是否结束训练
        lmin = self.lmin  # 批的最短匹配长度
        lmax = self.lmax  # 批的最长匹配长度
        lastt = 0
        choice = 0
        for i in range(iter_time):  # 迭代次数：iter_time
            for j in range(lmin):  # 前lmin个时间窗不做处理
                t += 1
                state, rt, done = env.step(j)
                lt = state[2]  # 状态记录
            while t < H:  # 时间戳小于episode的长度
                lp = self.agent.get_next_action(state)  #根据Q表选取合适长度
                if lp == lt and lt != 0:  # 当切割长度 = 批的长度 进行匹配并更新Q表
                    last_state = state
                    state, rt, done = env.step(lp)  # 做动作后更新
                    self.time_window_length_check(env, state)
                    reward = rt
                    self.agent.update_q_table((last_state[0], last_state[1], last_state[2]), lp, reward, state)
                    choice = 1
                    lt = state[2]
                elif lp != lt and lt >= lmax:  # 当时间窗口到达最大窗口长度时，强制匹配
                    last_state = state
                    state, rt, done = env.step(lp)  # 做动作后更新
                    self.time_window_length_check(env, state)
                    reward = rt
                    self.agent.update_q_table((last_state[0], last_state[1], last_state[2]), lt, reward, state)
                    choice = 2
                    lt = state[2]
                else:  # 当切割长度 != 批的长度，向前进一
                    last_state = state
                    state, rt, done = env.step(lp)
                    self.time_window_length_check(env, state)
                    if done:
                        break
                    self.agent.update_q_table((last_state[0], last_state[1], last_state[2]), lp, rt, state)
                    choice = 3
                    lt = state[2]
                    t += 1
                    if t == 87:
                        print(1)
                        pass
                print(t)
            t = 0
            env.reset()  # 环境重置
            cargo_management.outbound = {}
        if env.start_date < env.train_end_date:
            env.change_train_data()

    def time_window_length_check(self,env:Environment,state:tuple):
        while state[2] not in self.agent.actions:
            env.batch.car_list.pop(0)
            env.change_batch_length()

    def train_by_day(self, iter_time:int):
        while env.start_date < env.train_end_date:
            global curr_config_class
            print('当前训练日期为:', env.start_date)
            env.cargo_date = env.start_date
            self.train(iter_time,len(env.car_list))
            self.agent.save_q_table(env.start_date)
        temp_df = pd.DataFrame(columns=['cut_length', 'car_cut_length'])
        temp_df['cut_length'] = env.cut_list
        temp_df['car_cut_length'] = env.car_cut_list
        temp_df.to_csv('/./data/FC/experiment/' + 'cut.csv')

        # temp_df.to_csv('/Users/lalala/Desktop/' + 'cut.csv')

    def test(self, car_list: List[Car]):
        is_spilt = False
        unbound_lp_list = None
        env.batch.car_list = car_list
        env.get_batch_length()
        if env.l >= env.lmax:
            env.batch.car_list = env.batch.car_list[0:len(env.batch.car_list) - 1]
            env.get_batch_length()
            is_spilt = True
            env.matcher.change_batch(env.batch)  # 换成要做匹配的批
            reward, match_list = env.matcher.km()
            unbound_lp_list = env.node_clear(match_list)
            env.change_batch_length()
            env.batch.car_list.append(car_list[len(car_list) - 1])
            env.cargo_date = car_list[0].arrive_time[0:8] + "000000"
            city_set = set()
            for i in range(len(env.batch.car_list)):
                for j in range(len(env.batch.car_list[i].city_list)):
                    city_set.add(env.batch.car_list[i].city_list[j])
            city_list = list(city_set)
            cargo_list = cargo_management.cargo_list_filter(condition=city_list)
            env.batch.load_plan_list = env.cargos_packaging(cargo_list)
            env.batch.city_load_plan_dict = env.get_load_plan_by_city(env.batch.load_plan_list)
            env.batch.cul_can_be_sent_load_plan_by_car()
            env.get_batch_length()
            env.state = (len(env.batch.car_list), len(env.batch.load_plan_list), env.l)
        else:
            env.cargo_date = car_list[0].arrive_time[0:8] + "000000"
            city_set = set()
            for i in range(len(car_list)):
                for j in range(len(car_list[i].city_list)):
                    city_set.add(car_list[i].city_list[j])
            city_list = list(city_set)
            cargo_list = cargo_management.cargo_list_filter(condition=city_list)
            env.batch.load_plan_list = env.cargos_packaging(cargo_list)
            env.batch.city_load_plan_dict = env.get_load_plan_by_city(env.batch.load_plan_list)
            env.batch.cul_can_be_sent_load_plan_by_car()
            env.get_batch_length()
            nl = len(env.batch.car_list)
            nr = len(env.batch.can_be_sent_load_plan)
            lp = self.agent.get_next_action((nl, nr, env.l))
            if lp == env.l:
                env.matcher.change_batch(env.batch)  # 换成要做匹配的批
                is_spilt = True
                reward, match_list = env.matcher.km()
                unbound_lp_list = env.node_clear(match_list)
                env.change_batch_length()  # 更新批长度
                env.state = (len(env.batch.car_list), len(env.batch.load_plan_list), env.l)
        return env.batch.car_list, is_spilt, unbound_lp_list

    def env_load_q_table(self,file_path:str):
        self.agent.load_Q_table(file_path)