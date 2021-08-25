# -*- coding: utf-8 -*-
# Description: 单车现场分货写数据库部分
# Created: liujiaye  2019/08/10
import pymysql
from config import config
from app.main.controller.config_name_management import curr_config_class
from _datetime import datetime
import time
import traceback
from flask import current_app
from app.utils.base_dao import BaseDao
from app.main.controller.config_name_management import loading_plan_id_increment
from app.tool.weight_value_calculation import weight_value_calculate


class AllocationDao(BaseDao):

    def write_allocation_result(self, load_plan, create_time):
        try:
            load_plan_id = loading_plan_id_increment()
            matching_value = weight_value_calculate(load_plan.car, load_plan)
            sql = "insert into loading_plan_main " \
                  "(id,car_mark,city,sum_weight,create_time,priority,arrive_time,matching_value)" \
                  "values('{0}','{1}','{2}',{3},'{4}',{5},'{6}',{7})".format(
                str(load_plan_id), str(load_plan.car.license_plate_number), str(load_plan.car.city), load_plan.load
                , str(create_time), float(load_plan.priority), str(load_plan.car.arrive_time), matching_value
            )
            # print(sql)
            self.execute(sql)
            for c in load_plan.cargo_list:
                sql = "insert into loading_plan_detail " \
                      "(id,car_mark,order_number,shipping,out_stock,unloading_address," \
                      "prod_name,weight,count,priority)" \
                      "values('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}','{9}')".format(
                    str(load_plan_id), str(load_plan.car.license_plate_number), str(c.order_number), str(c.shipping),
                    str(c.out_stock), str(c.unloading_address), str(c.prod_name), str(c.c_weight), str(c.c_count),
                    str(c.priority))
                # print(sql)
                self.execute(sql)

        except Exception as e:
            # conn.close()
            traceback.print_exc()
            current_app.logger.info("write allocation error")
            current_app.logger.exception(e)

    def write_main(self, load_plan, create_time):
        try:
            load_plan_id = loading_plan_id_increment()
            matching_value = weight_value_calculate(load_plan.car, load_plan)
            if load_plan.load > 36:
                load_plan.load = 0.0
            sql = "insert into loading_plan_main " \
                  "(id,car_mark,city,sum_weight,create_time,priority,arrive_time,matching_value)" \
                  "values('{0}','{1}','{2}',{3},'{4}',{5},'{6}',{7})".format(
                str(load_plan_id), str(load_plan.car.license_plate_number), str(load_plan.car.city), load_plan.load
                , str(create_time), float(load_plan.priority), str(load_plan.car.arrive_time), matching_value
            )
            # print(sql)
            self.execute(sql)

        except Exception as e:
            # conn.close()
            traceback.print_exc()
            current_app.logger.info("write allocation error")
            current_app.logger.exception(e)


allocation_dao = AllocationDao()
