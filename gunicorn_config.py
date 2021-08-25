# -*- coding: utf-8 -*-
# Description: Gunicorn服务器配置文件
# Created: yangyingjie 2019/06/19
# Modified: yangyingjie 2019/06/19; yangyingjie 2019/06/20

from gevent import monkey
import multiprocessing

# 单进程的异步编程模型称为协程。gevent是把python同步代码变成异步协程的第三方库。
# gevent的monkey patch在执行时将标准库中的thread/socket等动态替换为非阻塞的模块。
monkey.patch_all()

# 应用参数
APP_NAME = 'models-goods-allocation'
SERVER_PORT = 9206

# 配置参数
bind = '127.0.0.1:{}'.format(SERVER_PORT)
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = 'gevent'
worker_connections = 1000
timeout = 120
backlog = 2048
debug = True
proc_name = 'gunicorn_app'
pidfile = '/app/{}/logs/gunicorn.pid'.format(APP_NAME)
capture_output = True
logfile = '/app/{}/logs/gunicorn.log'.format(APP_NAME)
# 访问日志格式，错误日志无法设置
"""
其每个选项的含义如下：
h          remote address
l          '-'
u          currently '-', may be main name in future releases
t          date of the request
r          status line (e.g. ``GET / HTTP/1.1``)
s          status
b          response length or '-'
f          referer
a          main agent
T          request time in seconds
D          request time in microseconds
L          request time in decimal seconds
p          process ID
"""
access_log_format = \
    '%(t)s %(p)s %(h)s "%(r)s" %(s)s %(L)s %(b)s %(f)s" "%(a)s"'
# 访问日志文件
accesslog = '/app/{}/logs/gunicorn_access.log'.format(APP_NAME)

# 错误日志级别，访问日志级别无法设置
loglevel = 'debug'
# 错误日志文件
errorlog = '/app/{}/logs/gunicorn_server.log'.format(APP_NAME)

