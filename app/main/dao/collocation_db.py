# -*- coding: utf-8 -*-
# Description:
# Created: liujiaye  2019/08/12
from config import config
from app.main.controller.config_name_management import curr_config_class
import pymysql
import traceback
import pandas as pd
from app.main.entity.collocation import Collocation


def database_read_collocation(table, name):
    # try:
    #     read_sql = "select * from {0}".format(table)
    #     conn = pymysql.connect(
    #         host=config[curr_config_name].host_db,  # ip
    #         dao=config[curr_config_name].database_allocation,
    #         main=config[curr_config_name].user_db,  # 用户名
    #         password=config[curr_config_name].password_db,  # 密码
    #         port=config[curr_config_name].port_db,  # 端口号
    #     )
    #     entity = pd.read_sql(read_sql, conn)
    #     collocation_dic = {}
    #     for index, row in entity.iterrows():
    #         if row['main_' + name] in collocation_dic.keys():
    #             collocation_dic[row['main_' + name]].append_match(row['match_' + name], int(row['match_size']))
    #         else:
    #             collocation = Collocation(row['main_' + name])
    #             collocation.append_match(row['match_' + name], int(row['match_size']))
    #             collocation_dic[row['main_' + name]] = collocation
    #             # collocation.match_key_list = sorted(collocation.match_key.items(), key=lambda d: d[1], reverse=False)
    #             # collocation.update_match_order()
    #
    #     conn.close()
    #
    #     return collocation_dic
    # except:
    #     print("database_read_collocation error")
    #     traceback.print_exc()
    #     # conn.close()
    #     return {}
    # finally:
    #     conn.close()
    pass


def database_update_collocation(collocation_dic, database, type):
    '''
    更新t_commodity_collocation表
    :param collocation_dic:
    :return:
    '''
    # conn = pymysql.connect(
    #     host=config[curr_config_name].host_db,  # ip
    #     dao=config[curr_config_name].database_allocation,
    #     main=config[curr_config_name].user_db,  # 用户名
    #     password=config[curr_config_name].password_db,  # 密码
    #     port=config[curr_config_name].port_db,  # 端口号
    # )
    # cursor = conn.cursor()
    # for main in collocation_dic.keys():
    #     match_dic = collocation_dic[main].get_match_dic()
    #     for match in match_dic.keys():
    #         sql1 = "delete from {2} where main_{3}='{0}' and match_{3}='{1}'".format(
    #             main, match, dao, type)
    #         cursor.execute(sql1)
    #         sql2 = "insert into {3} values('{0}','{1}',{2})".format(main, match, match_dic[match], dao)
    #         cursor.execute(sql2)
    # cursor.connection.commit()
    # conn.close()
    pass
