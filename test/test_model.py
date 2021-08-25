# @Time :  14:23

# @Author : Hu Yaoyi

# @File : test_model.py

import os

import json
from datetime import datetime, timedelta
import requests
from app.main.controller.cargo_maintain import cargo_management


def test_end_window():
    requests.post('http://127.0.0.1:9206/stop')


def test_allocation(cars_list):
    '''
    1、给定车辆信息
    2、调用分货接口，进行单车现场分货，并将结果写入数据库
    :param:
    :return:
    '''
    for index, one_car in enumerate(cars_list):
        json_str = json.dumps(one_car)
        print(one_car)
        requests.post('http://127.0.0.1:9206/allocation', data=json_str)


def update_cargo_management(start_time):
    r = requests.post('http://127.0.0.1:9206/update_cargo_management', data=start_time)


# def evaluation_once_allocation(car_mark, arrive_time):
#     '''
#     1、分析单次分货的结果
#     分析指标：
#         单个车次之间订单流向距离
#         件数
#         是否为空车（）
#         是否为必发车次
#     :param load_task
#     :return:
#     '''
#
#     car_dict = {}
#     car_dict['license_plate_number'] = car_mark
#
#     read_loading_task_sql = "select * from db_trans_plan.loading_task_detail where license_plate_number = '{0}' and arrive_time = '{1}'".format(
#         car_mark, arrive_time)
#     loading_task = db.database_read(read_loading_task_sql, 'db_trans_plan')
#
#     # 单车的订单数，送货件数，送货重量
#     num_orders = len(loading_task[['order_num', 'out_warehouse']].drop_duplicates())
#     # print("发货订单数：", num_orders)
#     car_dict['num_orders'] = num_orders
#     send_count = loading_task['count'].sum()
#     # print("发货件数：", send_count)
#     car_dict['send_count'] = send_count
#     send_weight = loading_task['weight'].sum()
#     # print("发货重量：", send_weight)
#     car_dict['send_weight'] = send_weight
#
#     # 车辆的实际分货量
#     read_result_sql = "select * from db_trans_plan.loading_task_main where license_plate_number = '{0}' and arrive_time = '{1}'".format(
#         car_mark, arrive_time)
#     result = db.database_read(read_result_sql, 'db_trans_plan')
#     car_dict['plan_weight'] = result['plan_weight'].sum()
#
#     # 是否为必发
#     result['priority'] = result['priority'].astype('int')
#     if result['priority'].sum() > -2:
#         car_dict['priority'] = 1
#     else:
#         car_dict['priority'] = 0
#
#     read_loading_goods_sql = "select * from db_trans_plan.loading_goods_detail"
#     loading_goods = db.database_read(read_loading_goods_sql, 'db_trans_plan')
#     # print(loading_goods)
#
#     test_1 = loading_task[['loading_goods_id', 'order_num', 'out_warehouse', 'license_plate_number', 'weight', 'count']]
#     test_2 = loading_goods[['loading_goods_id', 'address']]
#     # print(test_1)
#     # print(test_2)
#     result_once = pd.merge(test_1, test_2, how='inner', on='loading_goods_id')
#     # print(result_once)
#     result_once = result_once.groupby(result_once['address'])[['weight']].sum()
#     # print(result_once)
#
#     address_list = result_once.index.tolist()
#     # print(address_list)
#     # 不同地址的数量
#     number_addresses = len(address_list)
#     car_dict['number_addresses'] = number_addresses
#
#     # 车辆地址，流向
#     if number_addresses > 1:
#         car_dict['address1'] = address_list[0]
#         car_dict['weight1'] = result_once.at[address_list[0], 'weight']
#         car_dict['address2'] = result_once.index[1]
#         car_dict['weight2'] = result_once.at[address_list[1], 'weight']
#
#     elif number_addresses == 1:
#         car_dict['address1'] = address_list[0]
#         car_dict['weight1'] = result_once.at[address_list[0], 'weight']
#         car_dict['address2'] = ''
#         car_dict['weight2'] = ''
#
#     # 不同地址之间的最大距离
#     max_distance = 0
#     for i in range(len(address_list)):
#         for j in range(i + 1, len(address_list)):
#             distance = get_distance(address_list[i], address_list[j])
#             if distance > max_distance:
#                 max_distance = distance
#
#     car_dict['max_distance'] = max_distance
#     return car_dict


# def fact_allocation_once(car_mark, arrive_time):
#     '''
#     分析每次实际的装车情况
#     车牌号，订单号，品名，重量，件数，流向（省市区）
#     :param car_mark:
#     :param arrive_time:
#     :return:
#     '''
#     # 读取实际的装车清单
#     fact_car_dict_all = []
#     arrive_time_2 = arrive_time[0:8]  # 日期
#     a = datetime.strptime(arrive_time_2, "%Y%m%d").date()
#     arrive_time_1 = int(arrive_time) + 1
#     arrive_time_1 = str(arrive_time_1)
#     print(arrive_time_1)
#
#     read_loading_main_sql = "select * from db_inter.bclp_bill_of_loading_no_main " \
#                             "where carmark = '{0}' and (create_time = '{1}'or create_time = '{2}')".format(car_mark,
#                                                                                                            arrive_time,
#                                                                                                            arrive_time_1)
#     fact_loading_main = db.database_read_produce(read_loading_main_sql, 'db_inter')
#     print(fact_loading_main)
#     fact_loading_main = fact_loading_main.iloc[0].tolist()
#     main_product_list_no = fact_loading_main[2]
#
#     read_loading_detail_sql = 'select * from db_inter.bclp_bill_of_loading_no_detail where main_product_list_no = {0}'.format(
#         main_product_list_no)
#     fact_loading_detail = db.database_read_produce(read_loading_detail_sql, 'db_inter')
#     for index, row in fact_loading_detail.iterrows():
#         fact_car_dict = {}
#         fact_car_dict['license_plate_number'] = car_mark
#         fact_car_dict['order_num'] = row['oritem_num']
#         fact_car_dict['commodity'] = row['commodity_name']
#         fact_car_dict['weight'] = row['weight']
#         fact_car_dict['count'] = row['count']
#         read_loading_no_sql = "select province, city, address, devperiod from db_inter.bclp_bill_of_loading_no where oritem_num = '{0}'".format(
#             row['oritem_num'])
#         fact_loading_no = db.database_read_produce(read_loading_no_sql, 'db_inter').iloc[0].tolist()
#         fact_car_dict['province'] = fact_loading_no[0]
#         fact_car_dict['city'] = fact_loading_no[1]
#         fact_car_dict['address'] = fact_loading_no[2]
#         b = datetime.strptime(fact_loading_no[3], "%Y%m%d").date()
#         if (a - b).days > -2:
#             fact_car_dict['priority'] = '1'
#         else:
#             fact_car_dict['priority'] = '0'
#         fact_car_dict_all.append(fact_car_dict)
#
#     return fact_car_dict_all
#

# def evaluation_allocation(start_time, end_time):
#     '''
#     1、分析一天的分货结果
#     分析指标：
#         一天出货重量
#         拼单率
#         必发车次占比
#         必发订单占比
#     :return:
#     '''
#     # 读取发货总表
#     read_result_sql = 'select * from db_trans_plan.loading_task_main where arrive_time between {0} and {1}'.format(
#         start_time, end_time)
#     result = db.database_read(read_result_sql, 'db_trans_plan')
#
#     # 发出总重量和总件数
#     weight = result['sum_weight'].sum()
#     print("该时段内发货总重量为：", weight)
#     plan_weight = result['plan_weight'].sum()
#     print("该时段内发货总重量为：", plan_weight)
#
#     count = result['sum_count'].sum()
#     print("该时段内发货总件数为：", count)
#
#     # 一天内完成的必发车次数和必发车次率
#     total = len(result)
#     print("该时段内发货总车次为：", total)
#     result['priority'] = result['priority'].astype('int')
#     priority_count = len(result[result['priority'] > -2])
#     print("该时段内必发车次为：", priority_count)
#     priority_rate = float(float(priority_count) / total)
#     print("该时段内必发车次率为：", priority_rate)
#
#     # 时段内必发订单占比
#     read_loading_goods_sql = "select * from db_trans_plan.loading_goods_detail where arrive_time between '{0}' and '{1}'".format(
#         start_time, end_time)
#     loading_goods = db.database_read(read_loading_goods_sql, 'db_trans_plan')
#
#     # 时段内完成的必发订单数量和占比
#     orders_total = len(loading_goods)
#     print("该时段内订单总数为：", orders_total)
#     loading_goods['priority'] = loading_goods['priority'].astype('int')
#     order_priority_count = len(loading_goods[loading_goods['priority'] > -2])
#     print("该时段内必发订单数为：", order_priority_count)
#     order_priority_rate = float(float(order_priority_count) / orders_total)
#     print("该时段内必发订单占比为：", order_priority_rate)


# def fact_allocation(start_time, end_time):
#     '''
#     1、分析一天的分货结果
#     分析指标：
#         一天出货重量
#         拼单率
#         必发车次占比
#         必发订单占比
#     :return:
#     '''
#     # 读取发货总表
#     read_fact_sql = 'select * from db_inter.bclp_bill_of_loading_no_detail where create_time between {0} and {1}'.format(
#         start_time, end_time)
#
#     result = db.database_read(read_fact_sql, 'db_inter').drop_duplicates()
#
#     # 发出总重量和总件数
#     result['weight'] = result['weight'].astype('float64')
#     result['count'] = result['count'].astype('int')
#     weight = result['weight'].sum()
#     print("该时段内发货总重量为：", weight)
#     count = result['count'].sum()
#     print("该时段内发货总件数为：", count)


if __name__ == '__main__':

    # with open("test.json", 'rb+') as load_f:
    #     test_car = json.load(load_f)
    # # print(test_car)
    #
    # test_car = test_car.get('entity')
    # test_allocation('20190702080000', test_car)

    json_file_name = ["7.2-18.json"]
    # json_file_name = ["070300.json", "070306.json", "070312.json", "070318.json"]
    start_time = ['20190702180100']
    # start_time = ['20190703000000', '20190703060000', '20190703120000', '20190703180000']

    for i in range(0, 1):
        end_time = datetime.strptime(start_time[i], "%Y%m%d%H%M%S") + timedelta(minutes=20)
        cargo_management.__init__(start_time[i])
        print(len(cargo_management.goods_dic))
        basedir = os.path.abspath(os.path.dirname(__file__))
        file_name = os.path.join(basedir, "", "json_data", json_file_name[i])
        with open(file_name, 'r', encoding='gbk') as load_f:
            test_car = json.load(load_f)
        test_allocation(test_car)

    # start_time = '20190702070000'
    # end_time = '20190703090000'
    # evaluation_allocation(start_time, end_time)
    # fact_allocation(start_time, end_time)

    # 测试结果输出
    # with open('0704.json', 'r', encoding='gb18030') as load_f:
    #     test_car = json.load(load_f)
    # print(test_car)
    # result_once = []
    # for index, one_car in enumerate(test_car):
    #     print(one_car)
    #     license_plate_number = one_car['license_plate_number']
    #     arrive_time = one_car['create_time']
    #     result = evaluation_once_allocation(license_plate_number, arrive_time)
    #     print(result)
    #     result_once.append(result)
    #
    # print(result_once)
    # result_once = pd.DataFrame(result_once)
    # result_once.to_csv('result_once_0704.csv', index=False, encoding='utf_8_sig')

    # 实际结果输出
    # fact_result_once = []
    # for index, one_car in enumerate(test_car):
    #     print(one_car)
    #     license_plate_number = one_car['license_plate_number']
    #     arrive_time = one_car['create_time']
    #     result = fact_allocation_once(license_plate_number, arrive_time)
    #     # print(result)
    #     for i in range(len(result)):
    #         fact_result_once.append(result[i])
    #
    # print(fact_result_once)
    # fact_result_once = pd.DataFrame(fact_result_once)
    # fact_result_once.to_csv('fact_result_once_0707.csv', index=False, encoding='utf_8_sig')
