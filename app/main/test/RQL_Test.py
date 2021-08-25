import pandas as pd

from app.tool.commodity_transform import CommodityTransform

res = pd.read_csv('C:/Users/93742/Desktop/bancheng.csv')
prod_name = list(res['prod_name'])
commodity_transform = CommodityTransform()
commodity_list = []
for i in range(len(prod_name)):
    name = commodity_transform.change_to_big(prod_name[i])
    commodity_list.append(name)


res['commodity'] = commodity_list

res.to_csv('C:/Users/93742/Desktop/chengpin.csv')
