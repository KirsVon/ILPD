#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# @Project  ：Dispatch-of-Goods 
# @File     ：test_history.py
# @Author   ：liujiaye
# @Date     ：2021/3/28 10:48
from app.main.models.heuristic_algorithm import Heuristic
from app.main.dao.allocation_db import allocation_dao
from app.main.dao.load_plan_dao import load_plan_dao

import app.main.controller.config_name_management as cm
import pandas as pd
from app.main.entity.car import Car
from app.main.entity.cargo import Cargo
from app.tool.car_to_load_plan import get_load_plan_by_virtual_car
from datetime import datetime, timedelta
from app.main.controller.cargo_maintain import cargo_management

if __name__ == '__main__':
    day_str = "20201016000000"
    end_day_str = "20201016235959"
    # 获取车辆
    car_list = []
    data = pd.read_csv(cm.curr_config_class.CAR_DATA_ROOT_DIRECTORY + day_str + ".csv")
    car_dict_list = data.to_dict(orient="records")
    license_plate_number_dict = {}
    for car in car_dict_list:
        temp = Car()
        temp.set_attr(car)
        index_begin = temp.city.find("[")
        index_end = temp.city.find("]")
        if index_begin != -1:
            temp.city = temp.city[index_begin + 2:index_end - 1] + '市'
            # print(temp.city)
        car_list.append(temp)
        if temp.license_plate_number not in license_plate_number_dict:
            license_plate_number_dict[temp.license_plate_number] = [temp]
        else:
            license_plate_number_dict[temp.license_plate_number].append(temp)

    # 获取历史数据main、detail表
    # 读取历史数据-->load_plan_list
    load_plan_list = []
    history_car_dict = load_plan_dao.select_car(day_str, end_day_str)
    for i in history_car_dict:
        if i['license_plate_number'] in license_plate_number_dict:
            print(i['arrive_time'])
            num = i['main_product_list_no']
            cargos = load_plan_dao.select_load_plan(num)
            cargo_list = []
            for cargo in cargos:
                tmp = Cargo()
                tmp.set_attr(cargo)
                tmp.get_pri(day_str)
                cargo_list.append(tmp)
            tmp_load_plan = get_load_plan_by_virtual_car(cargo_list)
            tmp_load_plan.car = license_plate_number_dict[i['license_plate_number']][0]
            for car in license_plate_number_dict[i['license_plate_number']]:
                if car.arrive_time == i['arrive_time']:
                    tmp_load_plan.car = car
            tmp_load_plan.update_priority()
            load_plan_list.append(tmp_load_plan)

    for i in load_plan_list:
        allocation_dao.write_main(i, "20201015000000")
