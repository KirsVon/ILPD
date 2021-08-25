#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# @Project  ：Dispatch-of-Goods 
# @File     ：test_GA.py
# @Author   ：liujiaye
# @Date     ：2021/3/28 10:22
from app.main.entity.load_plan import LoadPlan
from app.main.models.heuristic_algorithm import Heuristic
from app.main.dao.allocation_db import allocation_dao
import app.main.controller.config_name_management as cm
import pandas as pd
from app.main.entity.car import Car
from datetime import datetime, timedelta
from app.main.controller.cargo_maintain import cargo_management
from app.main.controller.config_name_management import curr_config_class

if __name__ == '__main__':
    day_str = "20201015000000"
    # cargo_management.init_cargo_dic(start_time, 2)
    # 读取车辆
    car_list = []
    data = pd.read_csv(cm.curr_config_class.CAR_DATA_ROOT_DIRECTORY + day_str + ".csv")
    car_dict_list = data.to_dict(orient="records")
    load_plan_list = []
    for car in car_dict_list:
        temp = Car()
        temp.set_attr(car)
        index_begin = temp.city.find("[")
        index_end = temp.city.find("]")
        if index_begin != -1:
            temp.city = temp.city[index_begin + 2:index_end - 1] + '市'
            # print(temp.city)
        car_list.append(temp)
    # 20分钟循环
    time_period = datetime.strptime(day_str, "%Y%m%d%H%M%S") + timedelta(minutes=20)
    for car in car_list:
        print(car.arrive_time)
        curr_time = datetime.strptime(str(car.arrive_time), "%Y%m%d%H%M%S")
        if curr_time > time_period:
            time_period = time_period + timedelta(minutes=20)
            cargo_management.init_cargo_dic(time_period.strftime("%Y%m%d%H%M%S"))
        tmp_load_plan_list = Heuristic(car).distribution()
        tmp_load_plan = LoadPlan(car)
        if len(tmp_load_plan_list) != 0:
            tmp_load_plan = tmp_load_plan_list[0]
        cargo_management.add_status(tmp_load_plan)
        load_plan_list.append(tmp_load_plan)
    # for i in load_plan_list:
        allocation_dao.write_allocation_result(tmp_load_plan, tmp_load_plan.car.arrive_time)
    count = 0
    for key in cargo_management.cargo_dic.keys():
        if cargo_management.cargo_dic.get(key).c_weight < curr_config_class.MIN_LOAD_CAPACITY:
            count += 1
    print(count)
