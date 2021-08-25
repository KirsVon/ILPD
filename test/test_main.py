# -*- coding: utf-8 -*-
# Description:
# Created: 邵鲁玉  2019/10/07
from _datetime import datetime, timedelta
import json
from test.test_model import update_cargo_management, test_end_window, test_allocation
import os
from config import ExperimentalConfig


def test_main(start_day, start_day_str, days, start_time, times):
    '''
    测试：7月2日至7月6日每20分钟获取一次库存信息，单车分货所有真实的车辆装车清单（包含对已分货物的标记）
    '''
    i = start_day
    basedir = os.path.abspath(os.path.dirname(__file__))
    current_time = datetime.strptime(start_day_str, "%Y%m%d%H%M%S")
    while i < start_day + days:
        file_name = "070" + str(i) + ".json"
        file_path = os.path.join(basedir, "", "json_data", file_name)
        j = start_time
        with open(file_path, 'r', encoding='utf-8') as load_f:
            all_cars = json.load(load_f)
        while j < start_time + times:
            cars = []
            end_time = current_time + timedelta(minutes=20)
            print(current_time)
            # print(end_time)
            for index, one_car in enumerate(all_cars):
                car_time = datetime.strptime(one_car['create_time'], "%Y%m%d%H%M%S")
                if current_time <= car_time < end_time:
                    cars.append(one_car)
            # print("cars length:"+str(len(cars)))
            test_one_time_bin(cars, current_time)
            test_end_window()
            current_time = end_time
            j += 1
        i += 1


def test_one_time_bin(cars, start_time):
    '''
    一个20分钟的测试
    :param cars: 测试的车辆json
    :param start_time: 测试案例的开始时间 type:datetime
    :return:
    '''
    # end_time = datetime.strptime(start_time, ) + timedelta(minutes=20)
    # cargo_management.init_goods_list(start_time.strftime("%Y%m%d%H%M%S"))
    ExperimentalConfig.current_time_str = start_time
    update_cargo_management(start_time.strftime("%Y%m%d%H%M%S"))
    test_allocation(cars)


def test_demo(file_name, start_time):
    '''
    一个20分钟内的测试
    :param start_time:
    :return:
    '''
    basedir = os.path.abspath(os.path.dirname(__file__))
    file_path = os.path.join(basedir, "", "json_data", file_name)
    # , encoding = 'utf-8'
    with open(file_path, 'r') as load_f:
        cars = json.load(load_f)
    test_end_window()
    test_end_window()
    test_one_time_bin(cars, start_time)
    test_end_window()


if __name__ == '__main__':
    # 0740-->18+2
    test_main(4, "20190704000000", 3, 0, 3 * 24)
    # test_demo("debug.json", datetime.strptime("20190705050000", "%Y%m%d%H%M%S"))
    # test_main(5, "20190705000000", 1, 0, 1 * 24)
