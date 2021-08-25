# -*- coding: utf-8 -*-
# Description: 每个时间戳的duration（20分钟/1200秒）可能回来多个司机或者货物，所以需要用一个list来表示
#              将该时间戳单位化。
# Created: fengchong 2020/12/23
from app.main.entity.car import Car
from app.main.entity.cargo import Cargo
from app.main.entity.load_plan import LoadPlan


class Timestamp_Content:
    """
        Description: 包含该时间戳内来的货物清单，车辆清单
    """

    def __init__(self):
        self.car_list = []
        self.load_plan_list = []

    """
        Description: 扫描到Raw_data时，为该时间戳内的，加入该时间戳
    """
    def insert_car(self, car: Car):
        self.car_list.append(car)

    def insert_cargo(self, load_plan: LoadPlan):
        self.load_plan_list.append(LoadPlan)
