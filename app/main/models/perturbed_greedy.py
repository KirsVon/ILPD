#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：ILPD 
@File    ：perturbed_greedy.py
@IDE     ：PyCharm 
@Author  ：fengchong
@Date    ：2021/9/9 10:59 下午 
'''
import pandas as pd
import numpy as np
import random
from app.main.entity.car import Car
from app.main.controller.cargo_maintain import cargo_management
from app.main.entity.load_plan import LoadPlan
from datetime import datetime, timedelta
from app.main.controller.config_name_management import curr_config_class
from app.main.models.packaging import packaging


class Perturbed_Greedy():

    def __init__(self, start_date: str, end_date:str):
        self.car_list = [] # 单天车辆列表
        self.Current_Car = Car()  # 当前所要匹配车辆
        self.Current_Cargos = [] # 当前可发库存
        self.Current_Load_Plan = [] # 当前可以产生库存
        self.timestamp = 0
        self.current_time = datetime.strptime(start_date, '%Y%m%d%H%M%S')
        self.next_date = self.current_time + timedelta(days=1)
        self.end_time = datetime.strptime(end_date,'%Y%m%d%H%M%S')
        self.match_result = pd.DataFrame(columns=['carmark','weight','matching_time'])
        # 拉取车辆信息

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

    def load_cargo(self):
        try:
            # 若超过20分钟时间戳
            if datetime.strptime(str(int(self.Current_Car.arrive_time)), '%Y%m%d%H%M%S') >= self.current_time:
                print("拉取新数据, 时间为：", self.current_time)
                time_diff = timedelta(seconds=1200)
                self.current_time += time_diff
                self.Current_Cargos = cargo_management.cargo_list_filter(self.Current_Car.city_list)
                for i in range(len(self.Current_Cargos)):
                    self.Current_Cargos[i].get_pri(self.Current_Car.arrive_time)
                self.Current_Load_Plan = packaging(self.Current_Cargos)
                for i in range(len(self.Current_Load_Plan)):
                    self.Current_Load_Plan[i].update_priority()
            else:
                # 若未超过时间戳
                self.Current_Cargos = cargo_management.cargo_list_filter(self.Current_Car.city_list)
                for i in range(len(self.Current_Cargos)):
                    self.Current_Cargos[i].get_pri(self.Current_Car.arrive_time)
                self.Current_Load_Plan = packaging(self.Current_Cargos)
                for i in range(len(self.Current_Load_Plan)):
                    self.Current_Load_Plan[i].update_priority()
        except:
            pass
        finally:
            pass

    def sort(self,pertubed_list):
        """ 货物列表排序 """
        # 按优先级排序
        pertubed_list = sorted(pertubed_list, key=lambda cargo: cargo[1], reverse=True)
        return pertubed_list


    def pertubed_greedy_sort(self):
        pertubed_list = []
        for i in range(len(self.Current_Load_Plan)):
            value = np.exp(random.random()) * self.Current_Load_Plan[i].load
            pertubed_list.append((i,value))
        pertubed_list = self.sort(pertubed_list)
        return pertubed_list

    def pertubed_greedy_matching(self):
        while self.current_time < self.end_time:
            self.load_car(curr_config_class.CAR_DATA_ROOT_DIRECTORY + datetime.strftime(self.current_time,'%Y%m%d%H%M%S') + '.csv')
            self.timestamp = 0
            while self.timestamp < len(self.car_list):
                self.Current_Car = self.car_list[self.timestamp]
                self.load_cargo()
                pertubed_sorted_list = self.pertubed_greedy_sort()
                if len(pertubed_sorted_list) != 0:
                    best_individual = self.Current_Load_Plan.pop(pertubed_sorted_list[0][0])
                    self.match_result = self.match_result.append([{'carmark':self.Current_Car.license_plate_number,'weight':best_individual.load,'matching_time': self.Current_Car.arrive_time}])
                else:
                    self.match_result.append(([{'carmark':self.Current_Car.license_plate_number,'weight':0,'matching_time': self.Current_Car.arrive_time}]))
                self.timestamp += 1
            print(self.match_result)


