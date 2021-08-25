# -*- coding: utf-8 -*-
# Description:分货应用入口
# Created: liujiaye  2019/06/27

import logging
import os
import sys
from app import create_app

# 获取环境配置名称

config_name = os.getenv('FLASK_CONFIG') or 'default'

# 创建flask应用
app = create_app(config_name)

if __name__ != '__main__':
    # 如果不是直接运行，则将日志输出到 gunicorn 中
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)
    app.logger.info('config name = {} '.format(config_name))

if __name__ == '__main__':
    # 注：所有except模块，上线后所有报错中的print和traceback都可以删除，仅用于本地测试
    sys.setrecursionlimit(1000000000)
    app.logger.info('config name = {} '.format(config_name))
    server_port = app.config.get('SERVER_PORT')
    app.run(host='127.0.0.1', port=server_port, debug=True)
    # server_port = app.config.get('SERVER_PORT')
