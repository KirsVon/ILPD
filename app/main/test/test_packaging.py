#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# @Project  ：Dispatch-of-Goods 
# @File     ：test_packaging.py
# @Author   ：liujiaye
# @Date     ：2021/3/13 15:07
import pandas as pd
from app.main.entity.cargo import Cargo
from app.main.models.packaging import packaging


if __name__ == '__main__':
    def test_demo(filename):
        data = pd.read_csv(filename)
        records_dict_list = data.to_dict(orient="records")
        # print(type(records_dict_list))
        # print(type(records_dict_list[0]))
        cargo_list = []
        # 计算总重量
        sum_weight = 0.0
        for i in records_dict_list:
            cargo = Cargo()
            cargo.set_attr(i)
            cargo.get_priority()
            cargo_list.append(cargo)
            sum_weight += cargo.c_weight
        # packaging
        load_plan_list = packaging(cargo_list)
        # 对比封装前后重量
        print("装车清单数量" + str(len(load_plan_list)))
        load_plan_sum_weight = 0.0
        error_count = 0
        for load_plan in load_plan_list:
            load_plan_sum_weight += load_plan.load
            if load_plan.load < 29 or load_plan.load > 33:
                error_count += 1
        print("重量不在限制内的装车清单数量" + str(error_count))
        print("货物总重对比：" + str(sum_weight) + " : " + str(load_plan_sum_weight))
        # for l in tail_load_plan_list:
        #     print(l)

    # 20201010012000
    filename = "E:/test_data/20201010012000.csv"
    test_demo(filename)
    # for index in range(1, 6):
    #     starttime = datetime.datetime.now()
    #     filename = "E:/test_data/" + str(index) + ".csv"
    #     test_demo(filename)
    #     endtime = datetime.datetime.now()
    #     print((endtime - starttime).seconds)

    # 20200930070000
    # "E:/test_data/1.csv"
