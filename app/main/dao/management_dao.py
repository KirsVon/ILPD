# -*- coding: utf-8 -*-
# Description:
# Created: liujiaye  2019/07/09
from app.utils.base_dao import BaseDao

import traceback


class ManagementDao(BaseDao):
    def select_commodity(self):
        sql = """SELECT
                    prod_kind prod_name,
                    prod_kind_p1 commodity
                FROM
                   prod_corresponding_commodity """
        data = self.select_all(sql)
        commodities = {}
        for i in data:
            commodities[i['prod_name']] = i['commodity']
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
