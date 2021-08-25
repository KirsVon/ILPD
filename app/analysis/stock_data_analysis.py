# -*- coding: utf-8 -*-
# Description:
# Created: liujiaye  2020/08/11

from app.utils.db_pool import db_pool_ods
import traceback
import pymysql
from pymysql import MySQLError

from typing import List, Dict

from app.main.dao.stock_dao import stock_dao
from app.main.entity.cargo import Cargo

from datetime import datetime, timedelta
import pandas as pd


def history_stock_back(begin_time, end_time):
    """
    历史装车清单数据重新回归库存
    :param begin_time:
    :param end_time:
    :return:
    """
    cargo_data = stock_dao.select_out_stock_data(begin_time, end_time)
    cargo_list = list()
    for line in cargo_data:
        tmp_cargo = Cargo()
        tmp_cargo.set_attr(line)
        cargo_list.append(tmp_cargo)
    stock_dao.execute_add_stock(cargo_list)


# controller  stock_list

def get_daily_data_for_stock(day: str) -> Dict:
    '''

    获取当天（day）零点库存快照.from can_be_send_amount_daily
    :param day: 形如%Y%m%d%H%M%S
    :return: 返回stock对象
    '''
    daily_stock_data = stock_dao.select_stock_day_detail(day)
    daily_stock_list = []
    for line in daily_stock_data:
        tmp_cargo = Cargo()
        tmp_cargo.set_attr(line)
        tmp_cargo.time_period = datetime.strptime(tmp_cargo.time_period, "%d/%m/%Y").strftime("%Y%m%d%H%M%S")
        daily_stock_list.append(tmp_cargo)
    cargo_dic = dict()
    for cargo in daily_stock_list:
        if cargo.order_number + ',' + cargo.shipping + ',' + cargo.out_stock in cargo_dic:
            print("cargo key error : " + cargo.order_number + ',' + cargo.shipping + ',' + cargo.out_stock)
        else:
            cargo_dic[cargo.order_number + ',' + cargo.shipping + ',' + cargo.out_stock] = cargo
    return cargo_dic


def get_log_data_for_stock(date: datetime) -> List[Cargo]:
    '''
    按照时间点获取库存更新日志.from can_be_send_amount_log
    固定每20分钟更新
    :param date: string类型
    :return: 返回stock的更新日志数据
    '''
    date2 = date + timedelta(minutes=20)
    log_stock_data = stock_dao.select_stock_log(date.strftime("%Y%m%d%H%M%S"), date2.strftime("%Y%m%d%H%M%S"))
    log_stock_list = []
    for line in log_stock_data:
        tmp_cargo = Cargo()
        tmp_cargo.set_attr(line)
        log_stock_list.append(tmp_cargo)
    return log_stock_list


def get_stock_for_next_period(cargo_dic: Dict, date: str) -> Dict:
    '''
    根据当前库存列表与当前时刻，获取下个时段库存数据
    '''
    update_log = get_log_data_for_stock(date)
    # print(len(update_log))
    cargo_list_updated = merge_update_log(cargo_dic, update_log)

    return cargo_list_updated


def merge_update_log(cargo_dic, update_log) -> List[Cargo]:
    '''

    :param cargo_dic:
    :param update_log:
    :return:
    '''

    # update
    for cargo in update_log:
        if cargo.order_number + ',' + cargo.shipping + ',' + cargo.out_stock in cargo_dic:
            if cargo.status == "U" or cargo.status == "I":
                cargo_dic[cargo.order_number + ',' + cargo.shipping + ',' + cargo.out_stock] = cargo
            elif cargo.status == "D":
                del cargo_dic[cargo.order_number + ',' + cargo.shipping + ',' + cargo.out_stock]
        else:
            if cargo.status == 'D':
                continue
            cargo_dic[cargo.order_number + ',' + cargo.shipping + ',' + cargo.out_stock] = cargo

    # cargo_list = cargo_dic.values()
    return cargo_dic

    # # 创建字典实现两张表数据的时段对应，时段为key
    # daily_dic = dict()
    # log_dic = dict()
    # for s in daily_list:
    #     daily_dic.setdefault(s.time_period, []).append(s)
    # for s in update_log:
    #     log_dic.setdefault(s.time_period, []).append(s)
    # # 根据时间段遍历
    # # 以订单号+发货通知单号+出库仓库为主键进行一一对应查找遍历，并实现更新
    # cargo_dic = dict()
    #
    # for time_period in daily_dic:
    #     for cargo in daily_dic[time_period]:
    #         if cargo.order_number + ',' + cargo.shipping + ',' + cargo.out_stock in cargo_dic:
    #             print("cargo key error : " + cargo.order_number + ',' + cargo.shipping + ',' + cargo.out_stock)
    #         else:
    #             cargo_dic[cargo.order_number + ',' + cargo.shipping + ',' + cargo.out_stock] = cargo
    #     if time_period not in log_dic:
    #         print("log data lose time period : " + time_period)
    #         for cargo in cargo_dic:
    #             cargo_dic[cargo].time_period = date
    #         continue
    #     for cargo in log_dic[time_period]:
    #         if cargo.order_number + ',' + cargo.shipping + ',' + cargo.out_stock in cargo_dic:
    #             if cargo.status == "U" or cargo.status == "I":
    #                 cargo_dic[cargo.order_number + ',' + cargo.shipping + ',' + cargo.out_stock] = cargo
    #             elif cargo.status == "D":
    #                 del cargo_dic[cargo.order_number + ',' + cargo.shipping + ',' + cargo.out_stock]
    #         else:
    #             if cargo.status == 'D':
    #                 continue
    #             cargo_dic[cargo.order_number + ',' + cargo.shipping + ',' + cargo.out_stock] = cargo
    # cargo_list = cargo_dic.values()
    # return cargo_list


def to_csv(filename, cargo_list):
    data_list = []
    for i in cargo_list:
        data_list.append(i.as_dict())
    data = pd.DataFrame(data_list)
    # print(data.count())
    data.to_csv(filename)


if __name__ == '__main__':
    # =====================单元测试============================
    # date = "11/11/2020"
    # date1 = datetime.strptime(date, '%d/%m/%Y')  #
    # date2 = date1 + timedelta(minutes=20)
    # next_date = date2.strftime("%Y%m%d%H%M%S")
    # # output_stock_log_data(date, 10)
    #
    # stock_list = get_daily_data_for_stock(date)
    # print(len(stock_list))
    #
    # stock_list = get_stock_for_next_period(stock_list, date)
    # print(len(stock_list))
    # to_csv("E:/stockPer20/20201111000000.csv", stock_list)

    # =====================test==============================
    begin_date_str = "24/9/2020"
    end_date_str = "26/10/2020"
    begin_date = datetime.strptime(begin_date_str, '%d/%m/%Y')
    end_date = datetime.strptime(end_date_str, '%d/%m/%Y')
    next_date = begin_date + timedelta(days=1)
    filename = "E:/stockPer20_small_0226"

    while next_date < end_date:  # 月循环
        # print(begin_date.strftime('%#d/%#m/%Y'))
        tmp_begin_date = begin_date - timedelta(days=1)
        stock_dic = get_daily_data_for_stock(tmp_begin_date.strftime("%#d/%#m/%Y"))
        to_csv(filename + "/" + begin_date.strftime("%Y%m%d%H%M%S") + ".csv", stock_dic.values())
        curr_date = begin_date
        while curr_date <= next_date:
            stock_dic = get_stock_for_next_period(stock_dic, curr_date)
            to_csv(filename + "/" + curr_date.strftime("%Y%m%d%H%M%S") + ".csv", stock_dic.values())
            curr_date = curr_date + timedelta(minutes=20)
            print(curr_date)
        begin_date = next_date
        next_date = begin_date + timedelta(days=1)
