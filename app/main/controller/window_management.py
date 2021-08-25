# -*- coding: utf-8 -*-
# Description:
# Created: liujiaye  2019/11/25

from app.main.controller.distribution import Distribution
from app.main.dao.allocation_db import allocation_dao
from _datetime import datetime, timedelta
from app.main.entity.car import Car
import copy
import operator


class WindowManagement:
    max_window_size = timedelta(seconds=120)  # 最大（标准）窗口大小

    def __init__(self):
        # self.window_size_threshold = WindowManagement.max_window_size  # 3min
        self.distribution = Distribution(0)

    def add(self, car: Car):
        '''
        新的车辆请求到达时完成
        1.将新来的车辆增加到窗口图结构中
        2.判断窗口是否需要滑动
        3.判断窗口大小是否需要变动，变动分为增大和减小
        :param car:
        :return:
        '''
        return self.distribution.heuristic_distribution(car)

    def change_window_size(self):
        pass

    def finish(self):
        '''
        强制结束
        :return:
        '''
        pass


class Graph:
    path_id = 0

    def __init__(self):
        # 图结构：[<load_plan_id，load_plan_id>，]
        self.nodes = []  # type[[node1,node2,node3],[node1,node2]]
        self.path = {}  # {path_index:[node1,node2,node3]}
        self.mark_dic = {}  # {path_index:[cargo_id,]}
        self.create_time = datetime.now()
        self.end_time = datetime.now()
        self.window_size = self.end_time - self.create_time
        self.car_num = 0  # 窗口中的车辆的个数
        self.max_value = 0.0
        self.max_value_index = 0

    def create_graph(self, nodes):
        current_path = []
        for n in nodes:
            current_path.append([n])
        # print(current_path)
        self.update_graph(current_path)

    def append(self, nodes):
        '''
        增加结点s——装车清单候选集
        :param nodes:
        :return:
        '''
        tmp_path_list = []
        for path_index in self.path:
            for n in nodes:
                tmp_path = []
                can_connect = True
                for c in n.cargo_list:
                    if c.id in self.mark_dic[path_index]:
                        can_connect = False
                if can_connect:
                    tmp_path.extend(self.path[path_index])
                    tmp_path.append(n)
                    tmp_path_list.append(tmp_path)
                self.end_time = datetime.strptime(n.car.arrive_time, "%Y%m%d%H%M%S")
        self.update_graph(tmp_path_list)

    def reduce(self, slid_size):
        '''
        按步长缩减图
        :param slid_size:
        :return:
        '''
        pop_time = self.create_time + slid_size
        result = []
        index = 0
        if len(self.path) > 0:
            if self.max_value_index in self.path:
                if len(self.path[self.max_value_index]) > 0:
                    next_car = self.path[self.max_value_index][index]
                    result.append(next_car)
                    while index < len(self.path[self.max_value_index]):
                        next_car = self.path[self.max_value_index][index]
                        if datetime.strptime(next_car.car.arrive_time, "%Y%m%d%H%M%S") <= pop_time:
                            result.append(next_car)
                        else:
                            break
                        index += 1
                    tmp_paths = []
                    for path_index in self.path:
                        tmp_paths.append(self.path[path_index][index:])
                    self.update_graph(tmp_paths)
                    return result
        self.create_time = pop_time
        self.window_size = self.end_time - self.create_time
        return []

    def update_graph(self, paths):
        '''
        更新图
        :param paths: 已有路径->新节点=新路径
        :return:
        '''
        Graph.path_id = 0
        self.path = {}
        self.mark_dic = {}
        current_nodes = []
        paths_unique = list(set([tuple(t) for t in paths]))
        for p in paths_unique:
            tmp_priority = 0
            self.path[Graph.path_id] = p
            self.mark_dic[Graph.path_id] = []
            for n in p:
                if n not in current_nodes:
                    current_nodes.append(n)
                tmp_priority += n.priority
                for c in n.cargo_list:
                    if c.id not in self.mark_dic[Graph.path_id]:
                        self.mark_dic[Graph.path_id].append(c.id)
            if tmp_priority > self.max_value:
                self.max_value = tmp_priority
                self.max_value_index = Graph.path_id
            if len(p) != self.car_num:
                # print(str(self.car_num) + str(len(p)))
                self.car_num = len(p)
            if len(p) == 0:
                break
            if p[0].car.arrive_time != self.create_time.strftime("%Y%m%d%H%M%S"):
                # print(str(self.create_time) + str(p[0].car.arrive_time))
                self.create_time = datetime.strptime(p[0].car.arrive_time, "%Y%m%d%H%M%S")
            if p[-1].car.arrive_time != self.end_time.strftime("%Y%m%d%H%M%S"):
                # print(str(self.end_time) + str(p[-1].car.arrive_time))
                self.end_time = datetime.strptime(p[-1].car.arrive_time, "%Y%m%d%H%M%S")
            Graph.path_id += 1
        self.nodes.append(current_nodes)
        self.window_size = self.end_time - self.create_time


win_management = WindowManagement()
