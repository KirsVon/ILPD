# -*- coding: utf-8 -*-
# Description:
# Created: liujiaye  2019/07/10
import app.main.dao.collocation_db as db
from business_config import ModelConfig

# 得到可搭配的货物字典 commodity_collocation_dic
# commodity_collocation_dic格式：{main_commodity: Collocation对象,...} 即 {白卷： Collocation对象,...}
# commodity_collocation_dic = db.database_read_collocation('t_commodity_collocation', 'commodity')

# 得到可搭配的仓库字典 stock_collocation_dic
# stock_collocation_dic格式：{main_stock:Collocation对象,...} 即 {P5-P5冷轧成品库：Collocation对象,...}
# stock_collocation_dic = db.database_read_collocation('t_stock_collocation', 'stock')
stock_collocation_dic = ModelConfig.RG_WAREHOUSE_GROUP
city_collocation_dic = db.database_read_collocation('t_city_collocation', 'city')
