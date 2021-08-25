# -*- coding: utf-8 -*-
# Description:
# Created: liujiaye  2020/03/01
# Updated: fengchong 2020/12/13
import gym
import numpy as np
import pandas as pd
import sys
import logging
import math

from app.main.entity.batch import Batch
from app.main.entity.cargo import Cargo
from app.main.models.hungarian_algorithm import Hungarian_Algorithm
from app.main.models.packaging import packaging
from test.reinforcement_learning.entity.test_batch import test_batch
from test.reinforcement_learning.entity.test_car import test_car
from test.reinforcement_learning.entity.test_customer import test_customer
from app.main.models.kuhn_munkras import kuhn_munkras

logger = logging.getLogger(__name__)


class Env(gym.Env):

    def __init__(self, length_min: int, length_max: int, car_file_path: str, cargo_start_date:str):
        # 旧动作空间, 每件货按照commodity与district进行划分, 每个动作表示, 这个类别下取一件货
        # 新动作空间：l' ∈ [Lmin,Lmax]
        self.batch = Batch()
        self.lmin = length_min  # lmin批最短长度
        self.lmax = length_max  # lmax批最长长度
        self.C = length_max  # 左右节点的最大存在时间
        self.state = None  # 当前状态
        self.l = 0  # 批的长度
        self.timestamp = 0
        self.car_train_data = pd.read_csv(car_file_path)
        # self.cargo_train_data = pd.read_csv(cargo_file_path)
        self.cargo_list = []
        self.load_plan_list = []
        self.end = False
        self.action_space = []
        for i in range(0, self.lmax + 1):
            self.action_space.append(i)
        self.n_actions = len(self.action_space)
        # 旧状态空间, 表示的是每个类别下取了多少件货物, reward函数需要根据状态空间来计算当前的值
        # 新状态空间，表示为{<|车|,|货|>,l}         这里假定车与货的数量是小于批的长度的。
        self.observation_space = []
        for i in range(self.lmin, self.C):
            for j in range(i):
                for k in range(i):
                    self.observation_space.append((k, j, i))
        self.matcher = kuhn_munkras(self.batch, self.lmax, self.lmin)
        self.ha_matcher = Hungarian_Algorithm(self.batch)

    def cargo_packaging(self, cargo_data:pd.DataFrame):
        self.cargo_list = []
        records_dict_list = cargo_data.to_dict(orient="records")
        for i in records_dict_list:
            cargo = Cargo()
            cargo.set_attr(i)
            cargo.get_priority()
            self.cargo_list.append(cargo)
        self.load_plan_list = packaging(self.cargo_list)
        return self.load_plan_list


    def step(self, action: int):
        reward = 0
        done = False
        if action not in self.action_space:
            self.batch_forward()
            return self.state, reward, done
        # TODO reward规则待完善, 判断何时停止
        if action != self.l and self.l != self.lmax:
            self.batch_forward()
            if self.end == True:
                done = True
        elif action != self.l and self.l == self.lmax:
            self.matcher.change_batch(self.batch)
            reward, match_list = self.matcher.km()
            self.node_clear(match_list)
            self.l = max(len(self.batch.carlist), len(self.batch.customerlist))
            self.state = (len(self.batch.carlist), len(self.batch.customerlist), self.l)
            if self.end:
                done = True
        elif action == self.l:
            self.matcher.change_batch(self.batch)
            reward, match_list = self.matcher.km()
            self.node_clear(match_list)
            self.l = max(len(self.batch.carlist),len(self.batch.customerlist))
            # self.batch.carlist.clear()
            # self.batch.customerlist.clear()
            self.state = (len(self.batch.carlist), len(self.batch.customerlist), self.l)
            # self.batch_init()
            if self.end:
                done = True
        return self.state, reward, done

    def node_clear(self, match_list):
        nl = len(self.batch.carlist)
        nr = len(self.batch.customerlist)
        car_list = []
        customer_list = []
        if nl > nr:
            for i in range(nl):
                if match_list[i] == -1 or match_list[i] >= nl:
                    customer_list.append(self.batch.customerlist[i])
                if match_list[i] == -1 and i < nr:
                    customer_list.append(self.batch.customerlist[i])
                if i >= nr:
                    car_list.append(self.batch.carlist[match_list[i]])
        if nl < nr:
            car_set = set()
            for i in range(nr):
                if match_list[i] < nl:
                    car_set.add(match_list[i])
            for i in range(nl):
                if i not in car_set:
                    car_list.append(self.batch.carlist[i])
        self.batch.carlist = car_list
        self.batch.customerlist = customer_list

    def batch_init(self):
        '''
            RQL批初始化
        '''
        for i in range(self.lmin):
            try:
                che_is_come = self.car_train_data.loc[self.timestamp]['car_is_come']
                huo_is_come = self.car_train_data.loc[self.timestamp]['huo_is_come']
                che_id = self.car_train_data.loc[self.timestamp]['che']
                huo_id = self.car_train_data.loc[self.timestamp]['huo']
                if che_is_come != 0:
                    che = test_car(che_id, self.car_train_data.loc[self.timestamp]['che_x'],
                                   self.car_train_data.loc[self.timestamp]['che']['che_y'])
                    self.batch.insert_car(che)
                if huo_is_come != 0:
                    huo = test_customer(huo_id, self.car_train_data.loc[self.timestamp]['huo_x'],
                                        self.car_train_data.loc[self.timestamp]['huo_y'],
                                        self.car_train_data.loc[self.timestamp]['des_x'],
                                        self.car_train_data.loc[self.timestamp]['des_y'])
                    self.batch.insert_customer(huo)
                self.timestamp += 1
                self.l += 1
            except KeyError:
                self.end = True
                break
            finally:
                pass
        self.state = (len(self.batch.carlist), len(self.batch.customerlist), self.l)

    def batch_forward(self):
        try:
            che_is_come = self.car_train_data.loc[self.timestamp]['car_is_come']
            huo_is_come = self.car_train_data.loc[self.timestamp]['huo_is_come']
            che_id = self.car_train_data.loc[self.timestamp]['che']
            huo_id = self.car_train_data.loc[self.timestamp]['huo']
            if che_is_come != 0:
                che = test_car(che_id, self.car_train_data.loc[self.timestamp]['che_x'],
                               self.car_train_data.loc[self.timestamp]['che_y'])
                self.batch.insert_car(che)
            if huo_is_come != 0:
                huo = test_customer(huo_id, self.car_train_data.loc[self.timestamp]['huo_x'],
                                    self.car_train_data.loc[self.timestamp]['huo_y'],
                                    self.car_train_data.loc[self.timestamp]['des_x'],
                                    self.car_train_data.loc[self.timestamp]['des_y'])
                self.batch.insert_customer(huo)
            self.timestamp += 1
            self.l += 1
            self.state = (len(self.batch.carlist), len(self.batch.customerlist), self.l)
        except IndexError:
            self.end = True
        finally:
            pass

    def reset(self):
        # 将仓库状态随机化
        # self.state = np.zeros(self.n_actions)
        # self.counts = 0
        self.timestamp = 0
        return self.state

    def render(self, mode='human'):
        print('***************')
        return None

    def start(self):
        print('--成功加载环境--')

    def close(self):
        print('--成功关闭环境--')
        return None

    def clu_state(self, cargo_list):
        # self.state=cargo_list
        pass

    # def dfs(self,car:int,matrix_len:int,matrix:[[]]):
    #     self.vis_car[car] = True
    #     for i in range(matrix_len):
    #         if(self.vis_huo[i]):      #每一轮，每个顾客只尝试一次
    #             continue
    #         gap = self.ex_car[car] + self.ex_huo[i] - matrix[car][i]
    #         if gap == 0: #如果符合要求
    #             self.vis_huo[i] = True
    #             if self.match[i] == -1 or self.dfs(self.match[i],matrix_len,matrix):     #找到没有一个匹配的乘客 或者该乘客的司机可以找到其他人来接
    #                 self.match[i] = car
    #                 return True
    #         else:
    #             self.slack[i] = min(self.slack[i],gap) #slack理解为乘客想到让司机接到，还需要多少期望值。
    #     return False
    #
    #
    # def KM(self,batch:test_batch):
    #     car_num = len(self.batch.carlist)
    #     consumer_num = len(self.batch.customerlist)
    #     weight_matrix = [[0 for i in range(consumer_num)]for i in range(car_num)]
    #     for i in range(car_num):
    #         for j in range(consumer_num):
    #             dis_to_come = math.sqrt((self.batch.carlist[i]._loc_x - self.batch.customerlist[j]._loc_x)*(self.batch.carlist[i]._loc_x - self.batch.customerlist[j]._loc_x)+(self.batch.carlist[i]._loc_y - self.batch.customerlist[j]._loc_y)*(self.batch.carlist[i]._loc_y - self.batch.customerlist[j]._loc_y))
    #             if dis_to_come > 3:
    #                 weight_matrix[i][j] = -1
    #                 continue
    #             dis_to_go = math.sqrt((self.batch.customerlist[j]._des_x - self.batch.customerlist[j]._loc_x)*(self.batch.customerlist[j]._des_x - self.batch.customerlist[j]._loc_x)+(self.batch.customerlist[j]._des_y - self.batch.customerlist[j]._loc_y)*(self.batch.customerlist[j]._des_y - self.batch.customerlist[j]._loc_y))
    #             weight_matrix[i][j] = 14 - (dis_to_go + dis_to_come) * 0.57
    #             if dis_to_go > 3:
    #                 weight_matrix[i][j] += (dis_to_go - 3) * 2.4
    #     if car_num < consumer_num:                  # KM补零操作
    #         for i in range(consumer_num - car_num):
    #             added_list = []
    #             for j in range(consumer_num):
    #                 added_list.append(0)
    #             weight_matrix.append(added_list)
    #     elif consumer_num < car_num:
    #         for i in range(car_num):
    #             for j in range(car_num - consumer_num):
    #                 weight_matrix[i].append(0)
    #     matrix_len = max(car_num,consumer_num)
    #     self.match = [-1 for i in range(self.lmax)]  # 初始每个乘客都没有匹配到司机
    #     self.ex_huo = [0 for i in range(self.lmax)]  # 初始每个司机的期望值为0
    #
    #     # 每个司机的初始期望值是与他相连的乘客的最大订单价值期望。
    #     for i in range(matrix_len):
    #         self.ex_car[i] = weight_matrix[i][0]
    #         for j in range(matrix_len):
    #             self.ex_car[i] = max(self.ex_car[i],weight_matrix[i][j])
    #
    #     # 尝试解决每个司机拿到订单
    #     for i in range(matrix_len):
    #         self.slack = [sys.maxsize for i in range(self.lmax)]
    #         while True:
    #             # 为了解决司机订单的归宿问题：如果找不到就降低期望值，直到找到为止
    #             self.vis_car = [False for i in range(self.lmax)]
    #             self.vis_huo = [False for i in range(self.lmax)]
    #
    #             if self.dfs(i,matrix_len,weight_matrix):
    #                 break    # 如果找到司机，退出
    #             # 如果不能找到 就降低期望值
    #             # 最小可降低的期望值
    #             d = sys.maxsize
    #             for j in range(len(weight_matrix)):
    #                 if self.vis_huo[j] == False:
    #                     d = min(d,self.slack[j])
    #             for j in range(matrix_len):
    #                 # 所有访问过的司机降低期望值
    #                 if self.vis_car[j]:
    #                     self.ex_car[j] -= d
    #                 # 所有访问过的乘客增加期望值
    #                 if self.vis_huo[j]:
    #                     self.ex_huo[j] += d
    #                 else:
    #                     self.slack[j] -= d
    #     res = 0
    #     for i in range(matrix_len):
    #         res += weight_matrix[self.match[i]][i]
    #     return res
    #
    # def get_lmin(self):
    #     return self.lmin
