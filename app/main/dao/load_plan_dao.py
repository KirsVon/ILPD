#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# @Project  ：Dispatch-of-Goods 
# @File     ：load_plan_dao.py
# @Author   ：liujiaye
# @Date     ：2021/3/28 11:00
from app.utils.base_dao import BaseDao


class LoadPlanDao(BaseDao):
    def select_load_plan(self, main_product_list_no):
        sql = """SELECT
            main_product_list_no,
            oritem_num order_number,
            notice_num shipping,
            count c_count,
            weight c_weight,            
            outstock_name out_stock,
            alter_time time_period,
            alter_time can_send_date,
            commodity_name prod_name
        FROM
           load_detail9_10
        WHERE
            main_product_list_no='{0}'"""
        data = self.select_all(sql.format(main_product_list_no))
        # print(sql.format(day))
        return data

    def select_car(self, start_time, end_time):
        sql = """SELECT
            carmark license_plate_number,
            main_product_list_no,
            create_time arrive_time
        FROM
           load_main9_10
        WHERE
            create_time>='{0}'
            and
            create_time<='{1}'"""
        # print(sql.format(start_time, end_time))
        data = self.select_all(sql.format(start_time, end_time))
        return data


load_plan_dao = LoadPlanDao()
