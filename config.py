# -*- coding: utf-8 -*-
# Description: 应用配置文件
# Created: yangyingjie 2019/06/19
# Modified: yangyingjie 2019/06/19; yangyingjie 2019/06/20

import os

basedir = os.path.abspath(os.path.dirname(__file__))  # 获取绝对路径（返回文件路径）


class Config:
    """默认配置

    主要是数据库相关配置。
    SQLAlchemy是Python编程语言下的一款开源软件。提供了SQL工具包及对象关系映射（ORM）工具，使用MIT许可证发行。
    SQLAlchmey采用了类似于Java里Hibernate的数据映射模型，
    """
    # 应用参数
    APP_NAME = 'models-goods-allocation'
    SERVER_PORT = 9206
    #
    FLATPAGES_AUTO_RELOAD = True
    FLATPAGES_EXTENSION = '.md'
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'can you guess it'
    DEBUG = True
    # sqlalchemy两个主要配置
    # ORM底层所访问数据库URI
    SQLALCHEMY_DATABASE_URI = (
        'mysql+pymysql://v3dev_user2:V3dev!56@47.99.118.183:3306/'
        'db_trans_plan?charset=utf8')

    # 关闭数据库时是否自动提交事务
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    # 是否追踪修改
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    # 是否开启任务调度器,默认不开启
    SCHEDULER_OPEN = False
    # 任务调度器lock文件名称
    SCHEDULER_LOCK_FILE_NAME = 'scheduler-{}.lock'.format(APP_NAME)

    # 模型参数
    max_stock_size = 2
    max_unloading_address_size = 2
    load_bound = 2
    MAX_LOAD_CAPACITY = 36
    MIN_LOAD_CAPACITY = 29

    @staticmethod
    def init_app(app):
        pass


class ExperimentalConfig(Config):
    """实验环境配置
    """
    # 本地数据库连接
    LOCAL_MYSQL_HOST = 'localhost'
    LOCAL_MYSQL_PORT = 3306
    LOCAL_MYSQL_USER = 'root'
    LOCAL_MYSQL_PASSWD = ''
    LOCAL_MYSQL_DB = 'jingchuang'
    LOCAL_MYSQL_CHARSET = 'utf8'

    # 数仓连接
    ODS_MYSQL_HOST = 'am-bp117g8ua37t2f4vh90650.ads.aliyuncs.com'
    ODS_MYSQL_PORT = 3306
    ODS_MYSQL_USER = 'apiuser'
    ODS_MYSQL_PASSWD = 'reUa!0610'
    ODS_MYSQL_DB = 'db_ods'
    ODS_MYSQL_CHARSET = 'utf8'

    # Redis配置，可选（不使用时可删除）
    REDIS_HOST = '172.16.110.156'
    REDIS_PORT = '6379'
    REDIS_PASSWD = 'JCdev@56zh'
    REDIS_MAX_CONNECTIONS = 2

    # 微服务url
    DISPATCH_SERVICE_URL = 'http://192.168.1.70:9078'

    # APScheduler定时任务配置，可选（不使用时可删除）
    SCHEDULER_OPEN = False
    SCHEDULER_API_ENABLED = True


    # # 库存快照位置
    STOCK_DATA_ROOT_DIRECTORY_BY_DAY = "/Users/lalala/Desktop/experiment/data/stock/"
    # 库存快照位置
    STOCK_DATA_ROOT_DIRECTORY =  "/Users/lalala/Desktop/experiment/data/stock/"
    # Q表位置
    Q_TABLE_DIRECTORY =  " /Users/lalala/Desktop/experiment/data/20201009000000.csv"
    # 车辆数据位置
    CAR_DATA_ROOT_DIRECTORY = "/Users/lalala/Desktop/experiment/data/car_date/"
    # 品名转换文件
    PROD_CHANGE = "/Users/lalala/Desktop/experiment/data/prod_change.csv"
    # 司机历史各时间段频次
    DRIVER_FREQUENCY = "/Users/lalala/Desktop/experiment/data/driver_pri.csv"

# 库存快照位置
#     STOCK_DATA_ROOT_DIRECTORY_BY_DAY = "/./data/FC/stock/"
#     # 库存快照位置
#     STOCK_DATA_ROOT_DIRECTORY =  "/./data/FC/stock/"
#     # Q表位置
#     Q_TABLE_DIRECTORY =  "/./data/FC/experiment/0908/20201009000000.csv"
#     # 车辆数据位置
#     CAR_DATA_ROOT_DIRECTORY = "/./data/FC/car_date/"
#     # 品名转换文件
#     PROD_CHANGE = "/./data/FC/prod_change.csv"


class LocalConfig(Config):
    # 本地数据库连接
    LOCAL_MYSQL_HOST = 'localhost'
    LOCAL_MYSQL_PORT = 3306
    LOCAL_MYSQL_USER = 'root'
    LOCAL_MYSQL_PASSWD = 'liujiaye'
    LOCAL_MYSQL_DB = 'jingchuang'
    LOCAL_MYSQL_CHARSET = 'utf8'


# 设置环境配置映射
config = {
    'development': ExperimentalConfig,
    'default': ExperimentalConfig
}


def get_active_config():
    """获取当前生效的环境配置类

    :return: 生效的环境配置类
    """
    config_name = os.getenv('FLASK_CONFIG') or 'default'
    return config[config_name]


def get_active_config_name():
    """获取当前生效的环境配置名称
    :return: 生效的环境配置名称
    """
    config_name = os.getenv('FLASK_CONFIG') or 'default'
    return config_name
