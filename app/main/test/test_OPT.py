#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# @Project  ：Dispatch-of-Goods 
# @File     ：test_OPT.py
# @Author   ：liujiaye
# @Date     ：2021/3/26 22:32

from app.main.models.OPT import OPT
from app.main.dao.allocation_db import allocation_dao
import app.main.controller.config_name_management as cm
import pandas as pd
from app.main.entity.car import Car

if __name__ == '__main__':
    day_str = "20201016000000"
    # 读取车辆
    car_list = []
    data = pd.read_csv(cm.curr_config_class.CAR_DATA_ROOT_DIRECTORY + day_str + ".csv")
    car_dict_list = data.to_dict(orient="records")
    for car in car_dict_list:
        temp = Car()
        temp.set_attr(car)
        index_begin = temp.city.find("[")
        index_end = temp.city.find("]")
        if index_begin != -1:
            temp.city = temp.city[index_begin+2:index_end-1]+'市'
            # print(temp.city)
        car_list.append(temp)
    model = OPT(car_list)
    load_plan_list = model.distribution(day_str)
    for i in load_plan_list:
        allocation_dao.write_allocation_result(i, i.car.arrive_time)
