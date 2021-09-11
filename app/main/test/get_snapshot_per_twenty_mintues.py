#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：Dispatch-of-Goods-reinforcement-learning 
@File    ：get_snapshot_per_twenty_mintues.py
@IDE     ：PyCharm 
@Author  ：fengchong
@Date    ：2021/8/31 2:56 下午 
'''

from app.main.dao.snapshot_dao import snapshot_dao
from datetime import datetime
from datetime import timedelta
import time

current_time = datetime.now()
target_time = '2021-10-01 00:00:00'

while current_time < datetime.strptime(target_time, '%Y-%m-%d %H:%M:%S'):
    #time.sleep(1200)
    snapshot_dao.select_all_snapshot(datetime.strftime(current_time, '%Y-%m-%d %H:%M:%S'))
    print('存取数据, 当前时间为：', current_time)
    current_time += timedelta(seconds=1200)
    # if datetime.now() <= datetime.strptime(current_time, '%Y-%m-%d %H:%M:%S'):
    #     continue
    # else:
    #     print('存取数据')
    #     #snapshot_dao.select_all_snapshot()
    #     break

print(datetime.now())
# snapshot_dao.select_all_snapshot()