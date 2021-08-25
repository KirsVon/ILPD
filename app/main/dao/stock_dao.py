# -*- coding: utf-8 -*-
# Description:
# Created: liujiaye  2020/08/11
from app.utils.base_dao import BaseDao


class StockDao(BaseDao):
    def select_stock_day_detail(self, day):
        sql = """SELECT
            id,
            ORITEMNUM order_number,
            NOTICENUM shipping,
            WAINTFORDELNUMBER w_count, 
            WAINTFORDELWEIGHT w_weight, 
            CANSENDNUMBER c_count,
            CANSENDWEIGHT c_weight,            
            SUBSTRING_INDEX(DELIWAREHOUSE,'-',1) out_stock,
            DETAILADDRESS unloading_address,
            record_day time_period,
            CITY city,
            end_point district,
            ALTERTIME can_send_date,
            COMMODITYNAME prod_name,
            CONTACTNAME receiving_user
            
        FROM
           can_be_send_amount_daily
        WHERE
            record_day='{0}'"""
        data = self.select_all(sql.format(day))
        # print(sql.format(day))
        return data

    def select_stock_log(self, date1, date2):
        sql = """SELECT
            id,
            ORITEMNUM order_number,
            NOTICENUM shipping,
            WAINTFORDELNUMBER w_count, 
            WAINTFORDELWEIGHT w_weight, 
            CANSENDNUMBER c_count,
            CANSENDWEIGHT c_weight,            
            SUBSTRING_INDEX(DELIWAREHOUSE,'-',1) out_stock,
            DETAILADDRESS unloading_address,
            ALTERTIME can_send_date,
            CITY city,
            ADDRESS district,
            COMMODITYNAME prod_name,
            STATUS status
        FROM
           can_be_send_amount_log_small
        WHERE
            ALTERTIME>={0} and ALTERTIME<={1}"""
        data = self.select_all(sql.format(date1, date2))
        return data

    def execute_add_stock(self, cargo_list):
        # =================增加写数据库的sql====================
        sql = ""
        for i in cargo_list:
            sql += ""
        self.executemany(sql)

    def select_out_stock_data(self, begin_time,end_time):
        """
        读取历史装车清单数据
        :param begin_time:
        :param end_time:
        :return:
        """
        # =================修改sql====================
        sql = """SELECT
            id,
            ORITEMNUM order_number,
            NOTICENUM shipping,
            WAINTFORDELNUMBER w_count, 
            WAINTFORDELWEIGHT w_weight, 
            CANSENDNUMBER c_count,
            CANSENDWEIGHT c_weight,            
            SUBSTRING_INDEX(DELIWAREHOUSE,'-',1) out_stock,
            DETAILADDRESS unloading_address,
            CALCULATETIME time_period,
            CITY city,
            end_point district
        FROM
             
        WHERE
            CALCULATETIME>={0} and CALCULATETIME<={1}"""
        data = self.select_all(sql.format(begin_time,end_time))
        return data


stock_dao = StockDao()
