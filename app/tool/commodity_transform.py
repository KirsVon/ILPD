# -*- coding: utf-8 -*-
# Description:工具
# Created: liujiaye  2019/07/09

from app.main.dao.management_dao import management_dao
import pandas as pd

class CommodityTransform:
    '''
    大小品名转换工具
    '''

    def __init__(self):
        self.commodity_dic = management_dao.select_commodity()

    def change_to_big(self, commodity):
        if commodity in self.commodity_dic.keys():
            return self.commodity_dic[commodity]
        return None


commodity_transform = CommodityTransform()

if __name__ == '__main__':
    res = pd.read_csv('C:/Users/93742/Desktop/bancheng.csv')
    prod_name = list(res['prod_name'])
    commodity_transform = CommodityTransform()
    commodity_list = []
    for i in range(len(prod_name)):
        name = commodity_transform.change_to_big(prod_name[i])
        commodity_list.append(name)

    res['commodity'] = commodity_list
    res.dropna(subset=['commodity'], inplace=True)
    res.to_csv('C:/Users/93742/Desktop/chengpin.csv')