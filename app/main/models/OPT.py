# -*- coding: utf-8 -*-
# Description:
# Created: liujiaye  2019/12/21
from app.main.entity.car import Car
from app.main.entity.cargo import Cargo
from app.main.controller.cargo_maintain import cargo_management
from app.main.entity.load_plan import LoadPlan
from config import config
from app.main.controller.config_name_management import curr_config_class
import json
import copy


class OPT:
    def __init__(self, truck_list):
        self.truck_list = truck_list
        self.result = []

    def distribution(self, start_time):
        # init cargos
        cargo_management.init_cargo_dic(start_time, 2)
        for i in self.truck_list:
            cargo_list = cargo_management.cargo_list_filter([i.city])
            cargo_list = sorted(cargo_list, key=lambda cargo: cargo.priority, reverse=True)
            load_plan = LoadPlan(i)
            for c in cargo_list:
                mark = load_plan.add(c)
                if mark == -1:
                    tmp_cargo = copy.deepcopy(c)
                    tmp_cargo.c_weight = curr_config_class.MAX_LOAD_CAPACITY - load_plan.load
                    load_plan.add(tmp_cargo)
                    c.c_weight -= tmp_cargo.c_weight
                    break
            load_plan.update_priority()
            # cargo_management.add_status(load_plan)
            self.result.append(load_plan)
        return self.result

