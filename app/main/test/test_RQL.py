#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：Dispatch-of-Goods
@File ：test_JQL.py
@Author ：liujiaye
@Date ：2021/3/9 20:48
'''
from app.main.controller.time_window_management import TimeWindowManagement
import pandas as pd
import app.main.controller.config_name_management as cm
from _datetime import datetime, timedelta
from app.main.controller.cargo_maintain import cargo_management
from app.main.entity.car import Car
from app.main.controller.config_name_management import current_time_str
from app.main.controller.config_name_management import curr_config_class

def test_RQL():
    cm.current_time_str = day_str = "20201018000000"
    current_time_str = day_str
    cargo_management.init_cargo_dic(day_str)
    tim_win = TimeWindowManagement(day_str)
    data = pd.read_csv(cm.curr_config_class.CAR_DATA_ROOT_DIRECTORY + day_str + ".csv")
    car_dict_list = data.to_dict(orient="records")
    # 20分钟循环
    time_period = datetime.strptime(day_str, "%Y%m%d%H%M%S") + timedelta(minutes=20)
    for car in car_dict_list:
        tempcar = Car()
        tempcar.set_attr(car)
        index_begin = tempcar.city.find("[")
        index_end = tempcar.city.find("]")
        if index_begin != -1:
            tempcar.city = tempcar.city[index_begin + 2:index_end - 1] + '市'
            # print(temp.city)
        print(car["arrive_time"])
        curr_time = datetime.strptime(str(car["arrive_time"]), "%Y%m%d%H%M%S")
        if curr_time > time_period:
            cargo_management.init_cargo_dic(time_period.strftime("%Y%m%d%H%M%S"))
            time_period = time_period + timedelta(minutes=20)
        tim_win.add(tempcar)
    count = 0
    for key in cargo_management.cargo_dic.keys():
        if cargo_management.cargo_dic.get(key).c_weight < curr_config_class.MIN_LOAD_CAPACITY:
            count += 1
    print(count)

if __name__ == '__main__':
    test_RQL()
