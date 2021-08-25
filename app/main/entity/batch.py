# -*- coding: utf-8 -*-
# Description:车辆信息数据类
# Created: fengchong  2020/12/22
from app.main.entity.car  import Car
from app.main.entity.load_plan import LoadPlan
#from app.main.entity.timestamp_content import Timestamp_Content
from test.reinforcement_learning.entity.test_batch import test_batch


class Batch:
    """
        Description:初始化批内容：批的car_list、load_plan_list的内容为空
    """

    def __init__(self):
        self.car_list = []
        self.load_plan_list = []
        self.can_be_sent_load_plan = []
        self.city_load_plan_dict = dict()
    '''
        Description: 批中list加入元素
    '''

    def insert_car(self, one_car: Car):
        self.car_list.append(one_car)

    def insert_load_plan(self, one_load_plan: LoadPlan):
        self.load_plan_list.append(one_load_plan)

    def takeSecond(lp: LoadPlan):
        return lp.load


    def cul_can_be_sent_load_plan_by_car(self):
        car_city_dict = dict()
        for i in range(len(self.car_list)):
            for j in range(len(self.car_list[i].city_list)):
                if self.car_list[i].city_list[j] not in car_city_dict.keys():
                    car_city_dict[self.car_list[i].city_list[j]] = 1
                else:
                    count = car_city_dict.get(self.car_list[i].city_list[j]) + 1
                    car_city_dict[self.car_list[i].city_list[j]] = count
        can_be_sent_list = []
        city_list = list(car_city_dict.keys())

        for i in city_list:
            if i in self.city_load_plan_dict:
                if len(self.city_load_plan_dict[i]) > car_city_dict[i] * 10:
                    for j in range(car_city_dict[i] * 10):
                        can_be_sent_list.append(self.city_load_plan_dict[i][j])
                else:
                    for j in range(len(self.city_load_plan_dict[i])):
                        can_be_sent_list.append(self.city_load_plan_dict[i][j])
        self.can_be_sent_load_plan = can_be_sent_list