from typing import List
import app.main.models.packaging as p
from app.tool.can_collocate import can_collocate
from app.tool.car_to_load_plan import get_load_plan_by_car
import numpy as np


class HillClimbing:
    N = 10  # 迭代次数

    def __init__(self, car_list, load_plan_list):
        self.car_list = car_list
        self.load_plan_list = load_plan_list
        self.result = {}

    def run(self):
        """
        :return: load_plan_list 有实体car
        """

        # load plan list sort 按照装车清单的优先级降序排序
        load_plan_list = sorted(self.load_plan_list, key=lambda load_plan: load_plan.priority, reverse=True)
        # 1.取最大可能车辆——计算车辆和装车清单的匹配可能矩阵
        d = np.arange(len(self.car_list) * len(self.load_plan_list)) \
            .reshape((len(self.car_list), len(self.load_plan_list)))
        for i in range(self.car_list):
            for j in range(self.load_plan_list):
                d[i][j] = can_collocate(self.load_plan_list[j], get_load_plan_by_car(self.car_list[i]))

        # 2.初始化匹配
        # 初始化匹配
        init_result, selected_sequence = self.init()
        if len(self.car_list) > len(load_plan_list):
            print("cars size bigger than load plans")
            return init_result
        e = self.cul_e_score(init_result)
        # 3.遍历未获得订单的i车辆
        for turn in range(1, HillClimbing.N):
            i = 0
            while i < len(self.car_list):
                index = 0
                j = selected_sequence[i]
                # 4.找到均值更好的车进行替代
                while index < len(self.load_plan_list):
                    if j == index or (not d[i][j]) or (index in selected_sequence):
                        index += 1
                        continue
                    tmp_load_plan = self.load_plan_list[index]
                    tmp_load_plan.car = self.car_list[i]
                    past_load_plan = init_result[i]
                    init_result[i] = tmp_load_plan
                    if self.cul_e_score(init_result) > e:
                        selected_sequence[i] = index
                    else:
                        init_result[i] = past_load_plan
                    index += 1
        return init_result

    def probability(self):
        pass

    def init(self):
        i = 0
        result = []
        selected_sequence = []
        while i < len(self.car_list):
            find = False
            j = 0
            while j < len(self.load_plan_list) and (j not in selected_sequence):
                if can_collocate(self.load_plan_list[j], get_load_plan_by_car(self.car_list[i])):
                    self.load_plan_list[j].car = self.car_list[i]
                    result.append(self.load_plan_list[j])
                    find = True
                    selected_sequence.append(j)
                    break
                else:
                    j += 1
            if not find:
                print("初始化时，车辆未找到合适的装车清单")
                result.append(get_load_plan_by_car(self.car_list[i]))
        return result, selected_sequence

    @staticmethod
    def cul_e_score(load_plan_list):
        sum = 0
        for load_plan in load_plan_list:
            load_plan.update_priority()
            sum += load_plan.update_priority
        return sum / len(load_plan_list)
