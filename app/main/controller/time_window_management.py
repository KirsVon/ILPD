# -*- coding: utf-8 -*-
# Description:
# Created: liujiaye  2021/02/28
from app.main.controller.distribution import Distribution
from app.main.controller.window_management import WindowManagement
from app.main.controller.cargo_maintain import cargo_management
from app.main.dao.allocation_db import allocation_dao
from app.main.controller.config_name_management import model_type
from _datetime import datetime


class TimeWindowManagement(WindowManagement):
    def __init__(self, start_time):
        super().__init__()
        # self.window_size_threshold
        self.distribution = Distribution(0)
        self.car_list = []
        self.win_size = 0
        self.last_time = datetime.strptime(start_time, "%Y%m%d%H%M%S")

    def add(self, car):
        if model_type == 1:
            # JC_QL
            self.car_list.append(car)
            car_list, is_split, load_plan_list = self.distribution.model.test(self.car_list)
            if is_split:
                if len(load_plan_list) > 0:
                    create_time = datetime.strptime(load_plan_list[0].car.arrive_time, "%Y%m%d%H%M%S")
                else:
                    create_time = car.arrive_time
                for i in load_plan_list:
                    new_time = datetime.strptime(i.car.arrive_time, "%Y%m%d%H%M%S")
                    if new_time > create_time:
                        create_time = new_time
                for i in load_plan_list:
                    cargo_management.add_status(i)
                    allocation_dao.write_allocation_result(i, create_time.strftime("%Y%m%d%H%M%S"))
                self.car_list = car_list
            # self.last_time = car.arrive_time
        elif model_type == 2:
            # Hill_climbing
            self.win_size = int((datetime.strptime(car.arrive_time, "%Y%m%d%H%M%S") - self.last_time).seconds)
            self.win_size /= 60
            self.car_list.append(car)
            if self.win_size >= self.window_size_threshold:
                self.win_size = 0
                self.last_time = datetime.strptime(car.arrive_time, "%Y%m%d%H%M%S")
                load_plan_list = self.distribution.Hill_climbing(self.car_list)
                for i in load_plan_list:
                    cargo_management.add_status(i)
                    allocation_dao.write_allocation_result(i, car.arrive_time)
                self.car_list = []

    def finish(self, curr_time):
        is_split, load_plan_list = self.distribution.model.test(self.car_list)
        for i in load_plan_list:
            cargo_management.add_status(i)
            allocation_dao.write_allocation_result(i, curr_time)
        self.car_list = []
