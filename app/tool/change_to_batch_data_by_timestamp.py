# -*- coding: utf-8 -*-
# Description: 时间序列混乱的原数据转换成以时间戳为单位的批数据
# Created: fengchong 2020/12/22
from datetime import datetime
from datetime import timedelta
import pandas as pd
from typing import List

from app.main.entity.car import Car
from app.main.entity.load_plan import LoadPlan
from app.main.entity.timestamp_content import Timestamp_Content
from datetime import date

class Raw_to_Batch:
    """
        params: timestamp,时间戳单位：秒，秒数｜分，分数｜时、时数
    """

    def __init__(self, timestamp: str, company: int, data_car: pd.DataFrame):
        self.timestamp = timestamp
        self.company = company
        self.amount_second_per_timestamp = 0
        if timestamp == 'minute':
            self.amount_second_per_timestamp = 60 * company
        elif timestamp == 'hour':
            self.amount_second_per_timestamp = 3600 * company
        elif timestamp == 'second':
            self.amount_second_per_timestamp = company
        self.car_data = data_car
        self.car_data.sort_values(by="arrive_time",ascending=True, inplace=True)
        self.car_list = []
        records_dict_list = data_car.to_dict(orient="records")
        for i in records_dict_list:
            temp_car = Car()
            temp_car.set_attr(i)
            temp_car.set_commodity_list()
            temp_car.set_district_list()
            self.car_list.append(temp_car)
        # for index, row in data_car.iterrows():
        #     temp_car = Car(row["license_plate_number"], row["city"], row["district"], row["commodity"], row["arrive_time"])
        #     self.car_list.append(temp_car)
        # self.load_plan = data_load_plan
        self.pointer = 0
        self.timestamp_list = []

    """
            Description: 计算年份上，时间跨度
    """

    def Calculate_Time_Span(self, start: float, end: float,):
        begin = datetime.date(int(str(int(start))[0:4]), int(str(int(start))[4:6]), int(str(int(start))[6:8]))
        finish = datetime.date(int(str(int(end))[0:4]), int(str(int(end))[4:6]), int(str(int(end))[6:8]))
        return finish.__sub__(begin)


    """
        Description: 根据数据的时间跨度，生成对应的时间戳list
    """

    def generate_timestamp_by_car(self):
        arrive_time_list = list(self.car_data['arrive_time'])
        for i in range(len(arrive_time_list)):
            arrive_time_list[i] = str(int(arrive_time_list[i]))
        start_date = date(int(arrive_time_list[0][0:4]),int(arrive_time_list[0][4:6]),int(arrive_time_list[0][6:8]))
        end_date = date(int(str(int(arrive_time_list[len(arrive_time_list) - 1][0:8]) + 1)[0:4]),int(str(int(arrive_time_list[len(arrive_time_list) - 1][0:8]) + 1)[4:6]),int(str(int(arrive_time_list[len(arrive_time_list) - 1][0:8]) + 1)[6:8]))
        days = (end_date - start_date).days
        days_sum_second = days * 24 * 3600
        num_of_timestamp = int(days_sum_second / self.amount_second_per_timestamp)
        start_point = datetime.strptime(arrive_time_list[0][0:8] + '000000', '%Y%m%d%H%M%S')
        # end_point = datetime.strptime(arrive_time_list[len(arrive_time_list) - 1][0:8] + '235959', '%Y-%m-%d
        # %H:%M:%S')
        for i in range(num_of_timestamp):
            start_point += timedelta(seconds=self.amount_second_per_timestamp)
            t_c = Timestamp_Content()
            while datetime.strptime(arrive_time_list[self.pointer], '%Y%m%d%H%M%S').__lt__(start_point):
                t_c.insert_car(self.car_list[self.pointer])
                self.pointer += 1
                if self.pointer == len(arrive_time_list):
                    break
            self.timestamp_list.append(t_c)

    '''
        Description: 根据load_plan到达时间将load_plan数据加入时间戳类中
    '''

    # def add_load_plan_to_timestamp(self):
    #     self.load_plan.sort_values(by='arrive_time')
    #     arrive_time_list = list(self.load_plan['arrive_time'])
    #     start_point = datetime.strptime('20200901000000', '%Y%m%d%H%M%S')
    #     for i in range(len(arrive_time_list)):
    #         arrive_time_list[i] = str(int(arrive_time_list[i]))
    #         time_difference = datetime.strptime(str(arrive_time_list[i]), '%Y-%m-%d %H:%M:%S') - timedelta(seconds=self.amount_second_per_timestamp)
    #         index = int(time_difference / self.amount_second_per_timestamp)
    #         self.timestamp_list[index].insert_cargo(self.load_plan.iloc[i])

    def get_timestamp_data(self) -> List[Timestamp_Content]:
        self.generate_timestamp_by_car()
        # self.add_load_plan_to_timestamp()
        return  self.timestamp_list
