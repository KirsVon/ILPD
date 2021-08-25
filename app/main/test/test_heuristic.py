#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# @Project  ：Dispatch-of-Goods 
# @File     ：test_heuristic.py
# @Author   ：liujiaye
# @Date     ：2021/3/11 10:40
from app.main.controller.slide_window_management import SlideWindowManagement
import pandas as pd
import app.main.controller.config_name_management as cm
from _datetime import datetime, timedelta
from app.main.controller.cargo_maintain import cargo_management
from app.main.entity.car import Car


def test_heuristic():
    cm.current_time_str = day_str = "20201010000000"
    cargo_management.init_cargo_dic(day_str)
    tim_win = SlideWindowManagement()
    data = pd.read_csv(cm.curr_config_class.CAR_DATA_ROOT_DIRECTORY + day_str + ".csv")
    car_dict_list = data.to_dict(orient="records")
    # 20分钟循环
    time_period = datetime.strptime(day_str, "%Y%m%d%H%M%S") + timedelta(minutes=20)
    for car in car_dict_list:
        tempcar = Car()
        tempcar.set_attr(car)
        print(car["arrive_time"])
        curr_time = datetime.strptime(str(car["arrive_time"]), "%Y%m%d%H%M%S")
        if curr_time > time_period:
            time_period = time_period + timedelta(minutes=20)
            cargo_management.init_cargo_dic(time_period.strftime("%Y%m%d%H%M%S"))
        tim_win.add(tempcar)


if __name__ == '__main__':
    test_heuristic()
