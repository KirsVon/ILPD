#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：Dispatch-of-Goods-reinforcement-learning 
@File    ：snapshot_dao.py
@IDE     ：PyCharm 
@Author  ：fengchong
@Date    ：2021/8/31 2:36 下午 
'''
from app.utils.base_dao import BaseDao
from config import ExperimentalConfig
import pandas as pd


class snapshot_dao(BaseDao):
    def select_all_snapshot(self, time_str:str):
        sql = "select * from kc_rg_product_can_be_send_amount"
        data = self.select_all(sql)
        df = pd.DataFrame([data[0]])
        for i in range(1,len(data)):
            df_temp =pd.DataFrame([data[i]])
            df = pd.concat([df, df_temp])
        df.to_csv(ExperimentalConfig.STOCK_DATA_ROOT_DIRECTORY + time_str + '.csv')

snapshot_dao = snapshot_dao()
