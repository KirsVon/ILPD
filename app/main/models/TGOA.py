#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：ILPD 
@File    ：TGOA.py
@IDE     ：PyCharm 
@Author  ：fengchong
@Date    ：2021/9/15 9:29 上午 
'''
from typing import List

import pandas as pd
import numpy as np
import random
from app.main.entity.car import Car
from app.main.entity.batch import Batch
from app.main.controller.cargo_maintain import cargo_management
from app.main.entity.load_plan import LoadPlan
from datetime import datetime, timedelta
from app.main.controller.config_name_management import curr_config_class
from app.main.models.kuhn_munkras import kuhn_munkras
from app.main.models.packaging import packaging
import math
from copy import copy

lmax = 10
lmin = 1


class TGOA():
    def __init__(self, start_date:str, end_date:str):
        self.batch = Batch()
        self.car_list = []  # 单天车辆列表
        self.Current_Car = Car()  # 当前所要匹配车辆
        self.Current_Cargos = []  # 当前可发库存
        self.Current_Load_Plan = []  # 当前可以产生库存
        self.timestamp = 0
        self.timedelta = timedelta(minutes=20)
        self.timezone = ""
        self.current_time = datetime.strptime(start_date, '%Y%m%d%H%M%S')
        self.next_date = self.current_time + timedelta(days=1)
        self.end_time = datetime.strptime(end_date, '%Y%m%d%H%M%S')
        self.match_result = pd.DataFrame(columns=['carmark', 'weight', 'matching_time'])
        self.driver_frequency = {}
        self.get_driver_frequency()
        self.matcher = kuhn_munkras(self.batch, lmax, lmin)

    def get_timezone(self):
        self.timezone = datetime.strftime(self.current_time, "%Y%m%d%H%M%S")[8:14]
        temp = self.current_time + self.timedelta
        self.timezone += datetime.strftime(temp, "%Y%m%d%H%M%S")[8:14]
        return self.timezone

    def get_driver_frequency(self):
        dp_df = pd.read_csv(curr_config_class.DRIVER_FREQUENCY)
        timezone = list(dp_df['timezone'])
        frequency = list(dp_df['frequency'])
        for i in range(len(timezone)):
            timezone[i] = str(timezone[i])
            if len(timezone[i]) < 12:
                num = 12 - len(timezone[i])
                for j in range(num):
                    timezone[i] = '0' + timezone[i]
            self.driver_frequency[str(timezone[i])] = frequency[i]

    def load_car(self, car_file_path:str):
        self.car_list.clear()
        car_train_data = pd.read_csv(car_file_path)
        records_dict_list = car_train_data.to_dict(orient="records")
        for i in records_dict_list:
            temp_car = Car()
            temp_car.set_attr(i)
            temp_car.set_commodity_list()
            temp_car.set_district_list()
            temp_car.set_city_list()
            self.car_list.append(temp_car)
        print("车辆信息加载成功")

    def load_cargo(self,start_time:str):
        try:
            # 若超过20分钟时间戳
            cargo_management.init_cargo_dic(start_time)
            self.Current_Cargos = cargo_management.cargo_all()
            for i in range(len(self.Current_Cargos)):
                self.Current_Cargos[i].get_pri(start_time)
            self.Current_Load_Plan = packaging(self.Current_Cargos)
            for i in range(len(self.Current_Load_Plan)):
                self.Current_Load_Plan[i].update_priority()
            # if datetime.strptime(str(int(self.Current_Car.arrive_time)), '%Y%m%d%H%M%S') >= self.current_time:
            #     print("拉取新数据, 时间为：", self.current_time)
            #     time_diff = timedelta(seconds=1200)
            #     self.current_time += time_diff
            #     self.Current_Cargos = cargo_management.cargo_list_filter(self.Current_Car.city_list)
            #     for i in range(len(self.Current_Cargos)):
            #         self.Current_Cargos[i].get_pri(self.Current_Car.arrive_time)
            #     self.Current_Load_Plan = packaging(self.Current_Cargos)
            #     for i in range(len(self.Current_Load_Plan)):
            #         self.Current_Load_Plan[i].update_priority()
            # else:
            #     # 若未超过时间戳
            #     self.Current_Cargos = cargo_management.cargo_list_filter(self.Current_Car.city_list)
            #     for i in range(len(self.Current_Cargos)):
            #         self.Current_Cargos[i].get_pri(self.Current_Car.arrive_time)
            #     self.Current_Load_Plan = packaging(self.Current_Cargos)
            #     for i in range(len(self.Current_Load_Plan)):
            #         self.Current_Load_Plan[i].update_priority()
        except:
            pass
        finally:
            pass

    def screening_out_load_plan_by_car(self, car:Car):
        self.batch.load_plan_list = []
        for i in self.Current_Load_Plan:
            if i.car.city in car.city_list:
                self.batch.load_plan_list.append(copy(i))

    def screening_out_load_plan_by_carlist(self, car_list:List[Car]):
        self.batch.load_plan_list = []
        city_list = []
        for i in car_list:
            if i.city_list[0] not in city_list:
                city_list.append(i.city_list[0])
        for i in self.Current_Load_Plan:
            if i.cargo_list[0].city in city_list:
                self.batch.load_plan_list.append(copy(i))


    def sort(self, LoadPlan_list):
        """ LoadPlan列表排序 """
        # 按重量排序
        LoadPlan_list = sorted(LoadPlan_list, key=lambda loadplan: loadplan.load, reverse=True)
        return LoadPlan_list


    def TGOA(self):
        while self.current_time < self.end_time:
            self.load_car(curr_config_class.CAR_DATA_ROOT_DIRECTORY + datetime.strftime(self.current_time, '%Y%m%d%H%M%S') + '.csv')
            self.timestamp = 0
            while self.timestamp < len(self.car_list):
                self.load_cargo(datetime.strftime(self.current_time, '%Y%m%d%H%M%S'))
                m = math.floor(self.driver_frequency[self.get_timezone()])
                k = int(m / 2)
                count = 0
                while self.timestamp < len(self.car_list) and  count <= k:
                    if self.car_list[self.timestamp].arrive_time[8:14] >= self.timezone[0:6] and self.car_list[self.timestamp].arrive_time[8:14] <= self.timezone[6:12]:
                        self.screening_out_load_plan_by_car(self.car_list[self.timestamp])
                        LoadPlan_list = self.sort(self.batch.load_plan_list)
                        if len(LoadPlan_list) != 0:
                            self.match_result = self.match_result.append(([{'carmark':self.car_list[self.timestamp].license_plate_number,'weight':LoadPlan_list[0].load,'matching_time': self.car_list[self.timestamp].arrive_time}]))
                            bi = LoadPlan_list.pop(0)
                            self.drop_sent_load_plan([bi])
                            print('第', self.timestamp, '辆车匹配结果',{'carmark': self.Current_Car.license_plate_number, 'weight': bi.load,'matching_time': self.car_list[self.timestamp].arrive_time})
                        else:
                            self.match_result = self.match_result.append([{'carmark': self.car_list[self.timestamp].license_plate_number,'weight':0,'matching_time': self.car_list[self.timestamp].arrive_time}])
                            print('第', self.timestamp, '辆车未能匹配')
                    count += 1
                    self.timestamp += 1

                while self.timestamp < len(self.car_list) and  self.car_list[self.timestamp].arrive_time[8:14] >= self.timezone[0:6] and self.car_list[self.timestamp].arrive_time[8:14] <= self.timezone[6:12]:
                    self.batch.car_list.append(self.car_list[self.timestamp])
                    self.timestamp += 1
                if len(self.batch.car_list) != 0:
                    self.screening_out_load_plan_by_carlist(self.batch.car_list)
                    self.matcher.change_batch(self.batch)
                    #  can_be_sent_load_plan 有问题
                    reward, match_list = self.matcher.km()
                    match_lp_list = [-1 for i in range(len(self.batch.car_list))]
                    for i in range(max(len(self.batch.car_list), len(self.batch.can_be_sent_load_plan))):
                        if match_list[i] < len(self.batch.car_list):
                            match_lp_list[match_list[i]] = i
                    for i in range(len(self.batch.car_list)):
                        if match_lp_list[i] < len(self.batch.can_be_sent_load_plan):
                            self.match_result = self.match_result.append([{'carmark': self.batch.car_list[
                                i].license_plate_number, 'weight': self.batch.can_be_sent_load_plan[
                                match_lp_list[i]].load, 'matching_time': self.car_list[self.timestamp].arrive_time}])
                            print('第', self.timestamp, '辆车匹配结果',
                                  {'carmark': self.batch.car_list[i].license_plate_number,
                                   'weight': self.batch.can_be_sent_load_plan[match_lp_list[i]].load,
                                   'matching_time': self.car_list[self.timestamp].arrive_time})
                        else:
                            self.match_result = self.match_result.append([{'carmark': self.batch.car_list[
                                i].license_plate_number, 'weight': 0, 'matching_time': self.car_list[
                                self.timestamp].arrive_time}])
                            print('未能匹配')
                    unbound_lp_list = self.node_clear(match_list)
                    self.drop_sent_load_plan(unbound_lp_list)
                self.current_time += timedelta(minutes=20)
            self.match_result.to_csv('/Users/lalala/Desktop/experiment/result/TGOA/' + datetime.strftime(self.current_time,'%Y%m%d%H%M%S') + '.csv')


    def node_clear(self, match_list):
        nl = len(self.batch.car_list)
        nr = len(self.batch.can_be_sent_load_plan)
        car_list = []
        load_plan_list = []
        unbound_lp_list = []
        if nl < nr:
            car_set = set()
            lp_set = set()
            for i in range(nr):
                if match_list[i] < nl and match_list[i] >= 0:
                    car_set.add(match_list[i])
                    lp_set.add(i)
            for i in range(nl):
                if i not in car_set:
                    car_list.append(self.batch.car_list[i])
            for i in range(nr):
                if i not in lp_set:
                    load_plan_list.append(self.batch.can_be_sent_load_plan[i])
                else:
                    self.batch.can_be_sent_load_plan[i].car = self.batch.car_list[match_list[i]]
                    unbound_lp_list.append(self.batch.can_be_sent_load_plan[i])
        self.batch.car_list = car_list
        self.batch.can_be_sent_load_plan = load_plan_list
        return unbound_lp_list

    def drop_sent_load_plan(self, unbound_lp_list: List[LoadPlan]):
        for i in unbound_lp_list:
            cargo_management.add_status(i)
# 货物初始化会不会有问题？

