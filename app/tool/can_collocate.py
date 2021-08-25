# -*- coding: utf-8 -*-
# Description:
# Created: liujiaye  2019/07/10

# from app.analysis.collocation_analysis import commodity_collocation_dic
from app.analysis.collocation_analysis import stock_collocation_dic
from app.main.controller.config_name_management import curr_config_class


def commodity_can_collocate(commodity, commodity_list):
    if len(commodity_list) == 0:
        return True
    collocate = True
    for i in commodity_list:
        if commodity == i:
            return True
        # if commodity in commodity_collocation_dic.keys():
        #     if i not in commodity_collocation_dic[commodity].match_key.keys():
        #         collocate = False
        # else:
        #     collocate = False
    return collocate


def unloading_address_can_collocate(unloading_address, unloading_address_list):
    if len(unloading_address_list) == curr_config_class.max_unloading_address_size \
            and unloading_address in unloading_address_list:
        return True
    if len(unloading_address_list) >= curr_config_class.max_unloading_address_size:
        return False
    return True


def stock_can_collocate(stock, stock_list):
    stock_list.add(stock)
    for l in stock_collocation_dic:
        if stock in l:
            success = True
            for s in stock_list:
                if s not in l:
                    success = False
                    break
            if success:
                return True
    # if len(stock_list) == 0:
    #     return True
    # if len(stock_list) >= curr_config_class.max_stock_size and (stock not in stock_list):
    #     return False
    return True
    # collocate = True
    # for i in stock_list:
    #     if stock == i:
    #         return True
    #     # stock_collocation_dic格式：{main_stock: Collocation对象,...}
    #     # 即 {P5-P5冷轧成品库： Collocation对象, P7-剪切成品1库： Collocation对象,...}
    #     # Collocation对象中self.match_key的格式：{match_key:match_size}
    #     # 以 P5-P5冷轧成品库 为例即 {P6-P6冷轧成品库：36, P7-剪切成品1库：9,...}
    #     if stock in stock_collocation_dic.keys():
    #         if i not in stock_collocation_dic[stock].match_key.keys():#得到与它搭配的字典的key
    #             collocate = False
    #     else:
    #         collocate = False
    # return collocate


def is_outside_stock(stock):
    if stock == 'F20-运输处临港西库' or stock == 'F10-运输处临港东库':
        return True


def can_collocate(goods, load_task):
    # 装车清单已满则False
    if load_task.is_full:
        return False
    # # 货物线路不同于车辆信息中的线路则False
    # if goods.line_name != load_task.car.line_name:
    #     return False
    # 货物城市不同于车辆信息中的城市则False
    if goods.city != load_task.car.city:
        return False
    # 装车清单的卸货地址列表超过2个则False 或 等于2个 但此次货物的卸货地址并不在装车清单的卸货地址列表中
    if not unloading_address_can_collocate(goods.unloading_address, load_task.get_unloading_address_list()):
        return False
    # # 货物为外库 且车辆不去外库则False
    # if load_task.car.mark == '-' and is_outside_stock(goods.out_stock):
    #     return False
    # 货物的出库仓库的可搭配仓库  并没有在装车清单的仓库列表里 则False
    # 或者 装车清单的仓库列表大于2  又或者 装车清单等于2但货物的出库仓库不在列表中 = False
    if not stock_can_collocate(goods.out_stock, load_task.get_stock_list()):
        return False
    # # 货物的大品名的可搭配品种  并没有在装车清单的品名列表里 则False
    # if not commodity_can_collocate(goods.commodity, load_task.get_commodity_list()):
    #     return False
    # # 如果load_task的receiving_users 收货人列表中的不重复的个数少于2个 则可以添加货物
    # if not (len(set(load_task.receiving_users)) < 2 or (goods.receiving_user in load_task.receiving_users)):
    #     return False
    return True
