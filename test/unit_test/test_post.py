# -*- coding: utf-8 -*-
# Description:
# Created: liujiaye  2021/01/27

import json
import requests
from datetime import datetime, timedelta


class TestPost:
    @staticmethod
    def test_program_init(dict_data):
        # win_type = {"data": 1}
        json_str = json.dumps(dict_data)
        requests.post('http://127.0.0.1:9206/init', data=json_str)

    @staticmethod
    def test_end_window():
        requests.post('http://127.0.0.1:9206/stop')

    @staticmethod
    def test_allocation(car):
        """
        给定车辆信息,调用分货接口
        :param:
        :return:
        """
        json_str = json.dumps(car)
        # print(json_str)
        requests.post('http://127.0.0.1:9206/allocation', data=json_str)


    @staticmethod
    def update_cargo_management(start_time):
        """
        @param start_time:
        @return:
        """
        r = requests.post('http://127.0.0.1:9206/update_cargo_management', data=start_time)
