# -*- coding: utf-8 -*-
# Description:
# Created: liujiaye  2019/12/13

from app.main.models.JC_QL import JC_QL
# from app.main.models.RQL import RQL
from app.main.models.OPT import OPT
from app.main.models.RQL import RQL
from app.main.models.heuristic_algorithm import Heuristic
from app.main.models.hill_climbing_algorithm import HillClimbing
from app.main.controller.config_name_management import curr_config_class
from app.main.models.packaging import packaging
from app.main.controller.cargo_maintain import cargo_management


class Distribution:
    def __init__(self, choice: int):
        self.model = None
        if choice == 0:
            self.model = JC_QL()
            self.JC_QL_build()
        else:
            self.model = RQL()
            self.RQL_build()


    def heuristic_distribution(self, car):
        self.model = Heuristic(car)
        return self.model.distribution()

    def RQL(self):
        self.model = RQL()

    def OPT(self, car_list):
        return OPT(car_list)

    def Hill_climbing(self, car_list):
        load_plan_list = packaging(cargo_management.cargo_dic)
        return HillClimbing(car_list, load_plan_list)

    def RQL_build(self):
        self.model.agent.load_Q_table(curr_config_class.Q_TABLE_DIRECTORY)
        print(len(self.model.agent.q_table))

    def JC_QL_build(self):
        self.model.agent.load_Q_table(curr_config_class.Q_TABLE_DIRECTORY)
        print(len(self.model.agent.q_table))
