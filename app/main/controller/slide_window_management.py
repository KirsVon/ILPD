# -*- coding: utf-8 -*-
# Description:
# Created: liujiaye  2021/02/28
from app.main.controller.distribution import Distribution
from app.main.dao.allocation_db import allocation_dao
from _datetime import datetime, timedelta
from app.main.controller.cargo_maintain import cargo_management
from app.main.controller.window_management import WindowManagement, Graph


class SlideWindowManagement(WindowManagement):
    def __init__(self):
        self.window_size_threshold = WindowManagement.max_window_size  # 窗口大小 初始为5分钟
        self.slide_size = timedelta(seconds=30)  # 滑动窗口大小
        self.curr_window = Graph()  # 当前管理的窗口
        self.max_value_threshold = 2
        self.is_create = False
        super().__init__()

    def add(self, car):
        '''
        新的车辆请求到达时完成
        1.将新来的车辆增加到窗口图结构中
        2.判断窗口是否需要滑动
        3.判断窗口大小是否需要变动，变动分为增大和减小
        :param car:
        :return:
        '''
        load_plan_candidate_set = self.distribution.heuristic_distribution(car)
        if not self.is_create:
            self.curr_window.create_graph(load_plan_candidate_set)
            self.is_create = True
            return
        else:
            self.curr_window.append(load_plan_candidate_set)
        self.change_window_size()
        # 当前窗口是否滑动判断
        # 当当前窗口的大小大于等于阈值时，循环做窗口滑动（出队列操作），直至当前窗口大小小于阈值
        while self.curr_window.window_size >= self.window_size_threshold:
            end_time = self.curr_window.create_time \
                       + self.window_size_threshold
            load_plan_list = self.curr_window.reduce(self.slide_size)
            for i in load_plan_list:
                cargo_management.add_status(i)
                allocation_dao.write_allocation_result(i, end_time)

    def change_window_size(self):
        # 若窗口大小已经被缩减，则使用快慢速增长
        if self.window_size_threshold < WindowManagement.max_window_size:
            self.window_size_threshold *= 2
        else:
            self.window_size_threshold += self.slide_size
            if self.window_size_threshold > WindowManagement.max_window_size:
                self.window_size_threshold = WindowManagement.max_window_size
        # 若当前窗口大小未达到阈值，但是价值达到阈值，则立即调整窗口大小
        if self.curr_window.max_value > self.max_value_threshold \
                and self.curr_window.window_size < self.window_size_threshold:
            self.window_size_threshold = self.curr_window.window_size

    def finish(self):
        '''
        强制结束
        :return:
        '''
        while self.curr_window.window_size > timedelta(seconds=0):
            end_time = self.curr_window.create_time + self.window_size_threshold
            load_plan_list = self.curr_window.reduce(self.slide_size)
            for i in load_plan_list:
                allocation_dao.write_allocation_result(i, end_time)
        self.curr_window = Graph()
        self.is_create = False
