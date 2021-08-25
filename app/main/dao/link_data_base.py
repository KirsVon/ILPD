# -*- coding: utf-8 -*-
# Description:
# Created: liujiaye  2019/12/06
from app.main.controller.config_name_management import curr_config_class
from config import config
from sqlalchemy import create_engine


def link_data_base(sql, url_name):
    """
    连接数据库，执行sql语句
    返回查询结果
    """
    # try:
    #     connstr = config[curr_config_name].data_base_url[url_name]
    #     engine = create_engine(connstr, echo=False, max_overflow=5)
    #
    #     # 1 直接执行sql语句
    #     conn = engine.connect()
    #     entity = conn.execute(sql)
    #     conn.close()
    #     return entity.fetchall()
    # except SQLAlchemyError as e:
    #     current_app.logger.exception(e)
    #     return {"code": -1, "msg": ""}, 500
    return []
