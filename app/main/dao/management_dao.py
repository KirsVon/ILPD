# -*- coding: utf-8 -*-
# Description:
# Created: liujiaye  2019/07/09
# from app.utils.base_dao import BaseDao
import config
import pandas as pd

import traceback
from app.main.controller.config_name_management import curr_config_class

class ManagementDao():
    def select_commodity(self):
#         sql = """ SELECT
# DISTINCT
#  prod_kind,
# CASE
#
#  WHEN prod_kind_price_out RLIKE '型钢' THEN
#  '型钢'
#  WHEN prod_kind_price_out RLIKE '螺纹' THEN
#  '螺纹' ELSE prod_kind_price_out
#  END AS prod_kind_price_out
# FROM
#  db_sys_t_prod_spections ps
# WHERE
#  ps.company_id = 'C000000882'
#  AND is_use = 'SYBJ10'
#  AND prod_kind_price_out IS NOT NULL
# AND prod_kind_price_out != '' """
#         data = self.select_all(sql)
        data = pd.read_csv(curr_config_class.PROD_CHANGE)
        commodities = {}
        for index, row in data.iterrows():
            commodities[row['prod_kind']] = row['prod_kind_price_out']
        # connection.close()
        return commodities


management_dao = ManagementDao()

# def database_read(sql, dao):
#     '''
#         从数据库执行相应sql语句得到数据，并转换为dataframe格式
#         :param sql: sql语句
#         :param dao: 数据库
#         :return: 返回数据表，dataframe结构
#         '''
#     try:
#         connection = pymysql.connect(
#             host=config[curr_config_name].host_db,  # ip
#             dao=dao,
#             main=config[curr_config_name].user_db,  # 用户名
#             password=config[curr_config_name].password_db,  # 密码
#             port=config[curr_config_name].port_db,  # 端口号
#         )
#
#         # connection = pymysql.connect(
#         #     host=config[curr_config_name].host_inter,  # ip
#         #
#         #     dao=dao,
#         #     # 用户名
#         #     main=config[curr_config_name].user_inter,
#         #     # 密码
#         #     password=config[curr_config_name].password_inter,
#         #     # 端口号
#         #     port=config[curr_config_name].port_inter,
#         # )
#         entity = pd.read_sql(sql, connection)
#         connection.close()
#         return entity
#     except:
#         print(" database_read error")
#         traceback.print_exc()
#         connection.close()
#         return {}


# def database_read_produce(sql, dao):
#     '''
#         从数据库执行相应sql语句得到数据，并转换为dataframe格式
#         :param sql: sql语句
#         :param dao: 数据库
#         :return: 返回数据表，dataframe结构
#         '''
#     try:
#         development_conn = pymysql.connect(
#             host=config[curr_config_name].host_inter,  # ip
#             dao=dao,
#             main=config[curr_config_name].user_inter,  # 用户名
#             password=config[curr_config_name].password_inter,  # 密码
#             port=config[curr_config_name].port_inter,  # 端口号
#         )
#         entity = pd.read_sql(sql, development_conn)
#         development_conn.close()
#         return entity
#     except:
#         print(" database_read_produce error")
#         traceback.print_exc()
#         connection.close()
#         return {}
#
