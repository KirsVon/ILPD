# -*- coding: utf-8 -*-
# Description:
# Created: liujiaye  2019/06/27
# Last-Modified: liujiaye 2019/08/29

from app.main.entity.load_plan import LoadPlan
from app.main.entity.car import Car
from app.main.entity.cargo import Cargo
from app.main.controller.cargo_maintain import cargo_management
import copy
from app.main.controller.config_name_management import curr_config_class


class Heuristic:

    def __init__(self, car):
        '''
        构造函数
        :param car: 车辆信息json
        '''
        # essential entity
        self.car = Car()
        self.car.set_attr(car.as_dict())
        self.load_plan = LoadPlan(self.car)
        self.load_plan_candidate_set = []
        # 数据预处理
        # self.preprocessing(car)

    def distribution(self):
        '''
        分货功能：分出推荐车次（goods_list-->load_task），标记推荐车次，数据写库维护
        :return: self.load_task  type：LoadTask  推荐车次
        '''
        # 得到所有可装货物信息
        total_cargo_list = cargo_management.cargo_list_filter([self.car.city])
        cargo_list = []
        # 对cargo进行拆分，是的cargo_list中均为单件货物
        for c in total_cargo_list:
            while c.c_count > 1:
                tmp = Cargo()
                tmp.set_attr(c.as_dict())
                tmp.set_weight(c.unit_weight)
                cargo_list.append(tmp)
                c.set_weight(c.c_weight - c.unit_weight)
            if c.c_count == 1 and c.c_weight < curr_config_class.MAX_LOAD_CAPACITY:
                cargo_list.append(c)
        # 产生load plan候选集
        p = Population(cargo_list, self.car)
        self.load_plan_candidate_set = p.evolve()
        if len(self.load_plan_candidate_set) > 0:
            self.load_plan = self.load_plan_candidate_set[0]
        # write_allocation_result(self.load_plan)
        # cargo_management.add_my_status(self.load_task)  # 推荐分货结果增加标记
        # self.database_write()  # 写数据库
        return self.load_plan_candidate_set


class Population:
    topk = 5  # 控制候选集大小
    thr_set = 0.5  # 控制候选集均值
    thr_turn = 10  # 循环次数控制

    def __init__(self, cargo_list, car):
        self.car = car
        self.load_plan_list = []  # 当前轮次筛选后的所有load plan
        self.obsolete_cargo_list = cargo_list  # 丢弃的load plan中的货物-->废弃的基因，在变异时才启用
        self.turn = 0
        self.crossover_probability = 1

    def evolve(self):
        '''
        进化过程
        :return:
        '''
        self.initial_population()
        self.sift()
        if len(self.load_plan_list) == 1:
            return self.load_plan_list
        while self.evaluate() < self.thr_set and self.turn < self.thr_turn:
            new_load_plan_list = []
            self.load_plan_list = sorted(self.load_plan_list, key=lambda load_plan: load_plan.load, reverse=True)
            i = int(len(self.load_plan_list) / 2 - 1)
            j = int(len(self.load_plan_list) / 2)
            while i >= 0:
                new_load_plan = self.cross(self.load_plan_list[i], self.load_plan_list[j])
                new_load_plan = self.mutate(new_load_plan)
                new_load_plan_list.append(new_load_plan)
                i -= 1
                j += 1
            self.load_plan_list.extend(new_load_plan_list)
            self.sift()
        self.top_k()
        return self.load_plan_list

    def initial_population(self):
        '''
        初始化种群
        1.按照重量排序cargo_list（obsolete_cargo_list）
        2.顺序选取cargo产生load_plan_list，多余部分留在obsolete_cargo_list中
        :return:
        '''
        # 排序，按照重量排序
        self.obsolete_cargo_list = sorted(self.obsolete_cargo_list, key=lambda cargo: cargo.c_weight,
                                          reverse=True)
        # 顺序选取，将所有货物分发到load plan中
        load_plan_list = []
        index = 0
        last_end_index = 0
        cargo_list_mark = [0] * len(self.obsolete_cargo_list)  # 标记货物是否已经被选择
        loop = 0
        while 0 in cargo_list_mark and loop < 2*len(cargo_list_mark):
            loop += 1
            i = index
            load_plan = LoadPlan(self.car)
            load_plan_is_add = False
            while i < len(self.obsolete_cargo_list):
                if cargo_list_mark[i] != 1:  # 货物未被选择
                    result_type = load_plan.add(self.obsolete_cargo_list[i])  # 尝试增加货物
                    if result_type >= 0:  # 表示load plan 装满（满足下限）
                        cargo_list_mark[i] = 1
                        if load_plan.is_full:
                            #load_plan.update_load()
                            load_plan_list.append(load_plan)
                            load_plan_is_add = True
                            break
                    elif result_type == -1:  # 第一次被跳过的货物，标记跳过位置，下次从当前位置开始遍历
                        if last_end_index <= index:
                            last_end_index = i
                        if self.obsolete_cargo_list[-1].c_weight > curr_config_class.MAX_LOAD_CAPACITY - load_plan.load:
                            break
                i += 1
            if not load_plan_is_add:
                #load_plan.update_load()
                load_plan_list.append(load_plan)
            if last_end_index <= i:
                index = last_end_index
            else:
                index = i
        self.load_plan_list = load_plan_list

    def evaluate(self):
        '''
        当前种群均值
        :return: 函数值
        '''
        if len(self.load_plan_list) == 0:
            return 0
        else:
            return sum([item.load for item in self.load_plan_list]) / len(self.load_plan_list)

    def cross(self, load_plan1, load_plan2):
        '''
        交叉
        常规方法应该使用交叉概率与固定交叉规则进行交叉
        :param load_plan1:
        :param load_plan2:
        :return:
        '''
        better_load_plan = max(load_plan1, load_plan2, key=lambda load_plan: load_plan.load)
        worse_load_plan = min(load_plan1, load_plan2, key=lambda load_plan: load_plan.load)
        cargo_list1 = sorted(better_load_plan.cargo_list, key=lambda cargo: cargo.c_weight, reverse=True)
        cargo_list2 = sorted(worse_load_plan.cargo_list, key=lambda cargo: cargo.c_weight, reverse=True)
        need_change_cargo = cargo_list1[-1]
        load_limit = curr_config_class.MAX_LOAD_CAPACITY - better_load_plan.load + need_change_cargo.c_weight
        for cargo in cargo_list2:
            if need_change_cargo.c_weight <= cargo.c_weight <= load_limit \
                    and cargo.c_weight > need_change_cargo.c_weight:
                cargo_list1[-1] = cargo
                break
        result = LoadPlan(self.car)
        result.copy(cargo_list1)
        return result

    def mutate(self, load_plan):
        '''
        变异，使用已经淘汰的货物列表做变异
        需简化
        :param load_plan:
        :return:
        '''
        cargo_list = sorted(load_plan.cargo_list, key=lambda cargo: cargo.c_weight, reverse=True)
        need_change_cargo = cargo_list[-1]
        load_limit = curr_config_class.MAX_LOAD_CAPACITY - load_plan.load + need_change_cargo.c_weight
        for cargo in self.obsolete_cargo_list:
            if need_change_cargo.c_weight <= cargo.c_weight <= load_limit \
                    and cargo.c_weight > need_change_cargo.c_weight:
                cargo_list[-1] = cargo
                break
        result = LoadPlan(self.car)
        result.copy(cargo_list)
        return result

    def sift(self):
        '''
        筛选更优的个体，按照均值与轮数筛选
        :param load_plan_list:
        :return:
        '''
        tmp_obsolete_load_plan_list = []
        if len(self.load_plan_list) > 2 * self.topk:
            tmp_load_plan = []
            e = self.evaluate()
            for i in self.load_plan_list:
                if i.load >= e:
                    tmp_load_plan.append(i)
                else:
                    tmp_obsolete_load_plan_list.append(i)
            if len(tmp_load_plan) <= 1:
                tmp_obsolete_load_plan_list = self.load_plan_list[self.topk + 1:-1]
                self.top_k()
            else:
                self.load_plan_list = tmp_load_plan
        else:
            tmp_obsolete_load_plan_list = self.load_plan_list[self.topk + 1:-1]
            self.top_k()
        self.obsolete_cargo_list = []
        for lp in tmp_obsolete_load_plan_list:
            for c in lp.cargo_list:
                if c not in self.obsolete_cargo_list:
                    self.obsolete_cargo_list.append(c)
        self.turn += 1

    def top_k(self):
        self.load_plan_list = sorted(self.load_plan_list, key=lambda load_plan: load_plan.load, reverse=True)
        if len(self.load_plan_list) > self.topk:
            self.load_plan_list = self.load_plan_list[0:self.topk]
