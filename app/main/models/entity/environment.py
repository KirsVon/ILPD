# -*- coding: utf-8 -*-
# Description:
# Created: 冯冲 2020/12/22
from typing import List

import pandas as pd
from datetime import datetime
from datetime import timedelta

from app.main.entity.car import Car
from app.main.entity.load_plan import LoadPlan
from app.main.models.entity.base_environment import Env
from app.main.models.packaging import packaging
from app.main.controller.config_name_management import curr_config_class

from app.main.controller.cargo_maintain import cargo_management
from config import config


class Environment(Env):

    def __init__(self, min_length: int, max_length: int, car_file_path: str, cargo_date: str, end_date: str,
                 train_end_date: str):
        super().__init__(min_length, max_length, car_file_path, cargo_date)
        self.cargo_date = cargo_date
        self.start_date = cargo_date
        self.end_date = end_date
        self.car_list = []
        self.cut_list = []
        self.car_cut_list = []
        self.train_end_date = train_end_date
        records_dict_list = self.car_train_data.to_dict(orient="records")
        for i in records_dict_list:
            temp_car = Car()
            temp_car.set_attr(i)
            temp_car.set_commodity_list()
            temp_car.set_district_list()
            temp_car.set_city_list()
            self.car_list.append(temp_car)

    def get_day_cargo_dataframe(self):
        df_list = []
        temp_date = self.start_date
        while temp_date < self.end_date:
            df = pd.read_csv(curr_config_class.STOCK_DATA_ROOT_DIRECTORY_BY_DAY + temp_date[0:8] + '/' + temp_date + '.csv')
            temp_time = datetime.strptime(temp_date, '%Y%m%d%H%M%S')
            time_diff = timedelta(seconds=1200)
            temp_time += time_diff
            temp_date = datetime.strftime(temp_time, '%Y%m%d%H%M%S')
            df_list.append(df)
        return df_list

    def cargos_packaging(self, cargo_data: pd.DataFrame):
        self.cargo_list = []
        for i in range(len(cargo_data)):
            cargo_data[i].set_current_time(self.cargo_date)
            cargo_data[i].get_pri(self.cargo_date)
            self.cargo_list.append(cargo_data[i])
        self.load_plan_list = packaging(self.cargo_list)
        return self.load_plan_list


    def batch_forward(self, city_list: []):
        """
            Description: RQL批每向前走一步
        """
        delta = None
        mints = 0
        temp_car = self.car_list[self.timestamp]
        if len(self.batch.car_list) != 0:
            delta = datetime.strptime(str(int(temp_car.arrive_time)), '%Y%m%d%H%M%S') - datetime.strptime(str(int(self.batch.car_list[0].arrive_time)), '%Y%m%d%H%M%S')
            mints = int(delta.seconds / 60) + 1
        if mints < self.lmax:
            try:
                if str(int(temp_car.arrive_time)) >= self.cargo_date:
                    print('拉取新数据')
                    cargo_management.init_cargo_dic(self.cargo_date)
                    temp_time = datetime.strptime(self.cargo_date, '%Y%m%d%H%M%S')
                    time_diff = timedelta(seconds=1200)
                    temp_time += time_diff
                    self.cargo_date = datetime.strftime(temp_time, '%Y%m%d%H%M%S')
                city_set = set()
                for i in city_list:
                    city_set.add(i)
                for i in temp_car.city_list:
                    city_set.add(i)
                city_list = list(city_set)
                temp_cargo_list = cargo_management.cargo_list_filter(city_list)
                for i in range(len(temp_cargo_list)):
                    temp_cargo_list[i].get_pri(temp_car.arrive_time)
                temp_LP_list = packaging(temp_cargo_list)
                for i in range(len(temp_LP_list)):
                    temp_LP_list[i].update_priority()
                self.batch.load_plan_list = temp_LP_list
                self.batch.city_load_plan_dict = self.get_load_plan_by_city(temp_LP_list)
                self.batch.car_list.append(temp_car)
                self.batch.cul_can_be_sent_load_plan_by_car()
                self.timestamp += 1
                # delta = datetime.strptime(str(int(temp_car.arrive_time)), '%Y%m%d%H%M%S') - datetime.strptime(
                #     str(int(self.batch.car_list[0].arrive_time)), '%Y%m%d%H%M%S')
                # mints = int(delta.seconds / 60) + 1
                self.l = mints
                self.state = (len(self.batch.car_list), len(self.batch.can_be_sent_load_plan), self.l)
            except IndexError:
                self.end = True
            finally:
                return 1
        else:
            return 0



    def takeweight(self, elem:LoadPlan):
        return elem.load

    def get_load_plan_by_city(self, lp_list: List[LoadPlan]):
        city_lp_dict = dict()
        for i in lp_list:
            if i.car.city not in city_lp_dict.keys():
                city_lp_dict[i.car.city] = []
            else:
                temp_list = city_lp_dict[i.car.city]
                temp_list.append(i)
                city_lp_dict[i.car.city] = temp_list
        for k in city_lp_dict.keys():
            city_lp_dict[k].sort(reverse=True, key=self.takeweight)
        return city_lp_dict

    def node_clear(self, match_list):
        nl = len(self.batch.car_list)
        nr = len(self.batch.can_be_sent_load_plan)
        car_list = []
        load_plan_list = []
        unbound_lp_list = []
        if nl < nr:
            car_set = set()
            lp_set = set()
            for i in range(nr):
                if match_list[i] < nl and match_list[i] >= 0:
                    car_set.add(match_list[i])
                    lp_set.add(i)
            for i in range(nl):
                if i not in car_set:
                    car_list.append(self.batch.car_list[i])
            for i in range(nr):
                if i not in lp_set:
                    load_plan_list.append(self.batch.can_be_sent_load_plan[i])
                else:
                    self.batch.can_be_sent_load_plan[i].car = self.batch.car_list[match_list[i]]
                    unbound_lp_list.append(self.batch.can_be_sent_load_plan[i])
        self.batch.car_list = car_list
        self.batch.can_be_sent_load_plan = load_plan_list
        return unbound_lp_list

    def get_batch_length(self):
        if len(self.batch.car_list) == 0:
            self.l = 0
        else:
            mints = 0
            car_len = len(self.batch.car_list)
            delta = datetime.strptime(str(int(self.batch.car_list[car_len - 1].arrive_time)), '%Y%m%d%H%M%S') - datetime.strptime(
                str(int(self.batch.car_list[0].arrive_time)), '%Y%m%d%H%M%S')
            mints = int(delta.seconds / 60) + 1
            self.l = mints


    def change_batch_length(self):
        if len(self.batch.car_list) == 0:
            self.l = 0
        else:
            mints = 0
            delta = datetime.strptime(str(int(self.car_list[self.timestamp - 1].arrive_time)),
                                      '%Y%m%d%H%M%S') - datetime.strptime(
                str(int(self.batch.car_list[0].arrive_time)), '%Y%m%d%H%M%S')
            mints = int(delta.seconds / 60) + 1
            self.l = mints

    def reset(self):
        self.timestamp = 0
        self.cargo_date = self.start_date
        self.batch.car_list = []
        self.batch.can_be_sent_load_plan = []
        self.batch.load_plan_list = []
        self.batch.city_load_plan_dict = {}
        self.change_batch_length()
        return self.state

    def get_batch_car_city_list(self):
        city_list = []
        for i in self.batch.car_list:
            for j in i.city_list:
                city_list.append(j)
        return city_list

    def step(self, action: int):
        reward = 0
        done = False
        last_state = self.state
        if action not in self.action_space:
            res = self.batch_forward(self.get_batch_car_city_list())
            if res == 1:
                return self.state, reward, done
            else:
                self.matcher.change_batch(self.batch)
                print('开始匹配。。。')
                s_t = datetime.now()
                reward, match_list = self.matcher.km()
                self.car_cut_list.append(len(self.batch.car_list))
                unbound_lp_list = self.node_clear(match_list)
                self.drop_sent_load_plan(unbound_lp_list)
                e_t = datetime.now()
                cha = e_t - s_t
                print('结束匹配并更新,所耗时间：', cha.seconds)
                self.cut_list.append(self.l)
                self.change_batch_length()
                if self.state == last_state:
                    self.batch.car_list = []
                    self.change_batch_length()
                    self.state = (len(self.batch.car_list), len(self.batch.can_be_sent_load_plan), self.l)
                self.state = (len(self.batch.car_list), len(self.batch.can_be_sent_load_plan), self.l)
                if self.end:
                    done = True
        delta = None
        Flag = False
        if self.timestamp == len(self.car_list):
            print('why')
            pass
        if self.timestamp < len(self.car_list):
            if len(self.batch.car_list) == 0:
                delta = timedelta(seconds=0)
            else:
                delta = datetime.strptime(str(int(self.car_list[self.timestamp].arrive_time)),
                                          '%Y%m%d%H%M%S') - datetime.strptime(
                    str(int(self.batch.car_list[0].arrive_time)), '%Y%m%d%H%M%S')
        if action != self.l and self.l != self.lmax and int(delta.seconds / 60) < self.lmax:
            res = self.batch_forward(self.get_batch_car_city_list())
            if res == 1:
                return self.state, reward, done
            else:
                self.matcher.change_batch(self.batch)
                print('开始匹配。。。')
                s_t = datetime.now()
                reward, match_list = self.matcher.km()
                self.car_cut_list.append(len(self.batch.car_list))
                unbound_lp_list = self.node_clear(match_list)
                self.drop_sent_load_plan(unbound_lp_list)
                e_t = datetime.now()
                cha = e_t - s_t
                print('结束匹配并更新,所耗时间：', cha.seconds)
                self.cut_list.append(self.l)
                self.change_batch_length()
                if self.state == last_state:
                    self.batch.car_list = []
                    self.change_batch_length()
                    self.state = (len(self.batch.car_list), len(self.batch.can_be_sent_load_plan), self.l)
                self.state = (len(self.batch.car_list), len(self.batch.can_be_sent_load_plan), self.l)
                if self.end:
                    done = True
        elif (action != self.l and self.l == self.lmax and int(delta.seconds / 60) >= self.lmax) or (
                action != self.l and self.l != self.lmax and int(delta.seconds / 60) >= self.lmax):
            self.matcher.change_batch(self.batch)
            print('开始匹配。。。')
            s_t = datetime.now()
            reward, match_list = self.matcher.km()
            self.car_cut_list.append(len(self.batch.car_list))
            unbound_lp_list = self.node_clear(match_list)
            self.drop_sent_load_plan(unbound_lp_list)
            e_t = datetime.now()
            cha = e_t - s_t
            print('结束匹配并更新,所耗时间：', cha.seconds)
            self.cut_list.append(self.l)
            self.change_batch_length()
            if self.state == last_state:
                self.batch.car_list = []
                self.change_batch_length()
                self.state = (len(self.batch.car_list), len(self.batch.can_be_sent_load_plan), self.l)
            self.state = (len(self.batch.car_list), len(self.batch.can_be_sent_load_plan), self.l)
            if self.end:
                done = True
        elif action == self.l and len(self.batch.can_be_sent_load_plan) != 0 and len(self.batch.car_list) != 0:
            self.matcher.change_batch(self.batch)
            print('开始匹配。。。')
            reward, match_list = self.matcher.km()
            self.car_cut_list.append(len(self.batch.car_list))
            unbound_lp_list = self.node_clear(match_list)
            self.drop_sent_load_plan(unbound_lp_list)
            print('结束匹配并更新')
            self.cut_list.append(self.l)
            self.change_batch_length()
            if self.state == last_state:
                self.batch.car_list = []
                self.change_batch_length()
                self.state = (len(self.batch.car_list), len(self.batch.can_be_sent_load_plan), self.l)
            self.state = (len(self.batch.car_list), len(self.batch.can_be_sent_load_plan), self.l)
            if self.end:
                done = True
        elif len(self.batch.can_be_sent_load_plan) == 0:
            self.batch_forward(self.get_batch_car_city_list())
        elif len(self.batch.car_list) == 0:
            self.batch_forward(self.get_batch_car_city_list())
        return self.state, reward, done

    def drop_sent_load_plan(self, unbound_lp_list: List[LoadPlan]):
        for i in unbound_lp_list:
            cargo_management.add_status(i)

    def change_train_data(self):
        temp_date = datetime.strptime(self.start_date, '%Y%m%d%H%M%S')
        temp_date += timedelta(days=1)
        self.start_date = datetime.strftime(temp_date, '%Y%m%d%H%M%S')
        temp_date += timedelta(days=1)
        self.end_date = datetime.strftime(temp_date, '%Y%m%d%H%M%S')
        self.cargo_df_list = self.get_day_cargo_dataframe()
        self.car_train_data = pd.read_csv(curr_config_class.CAR_DATA_ROOT_DIRECTORY + self.start_date + '.csv')
        self.car_list = []
        records_dict_list = self.car_train_data.to_dict(orient="records")
        for i in records_dict_list:
            temp_car = Car()
            temp_car.set_attr(i)
            temp_car.set_commodity_list()
            temp_car.set_district_list()
            temp_car.set_city_list()
            self.car_list.append(temp_car)
