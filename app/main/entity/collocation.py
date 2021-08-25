# -*- coding: utf-8 -*-
# Description:
# Created: liujiaye  2019/07/08
import copy


class Collocation:
    ' 搭配类 '

    def __init__(self, key):
        # 货物大品名
        self.main_key = key
        # 可搭配的货物
        # self.match_key的格式：{match_key:match_size}
        self.match_key = dict()
        # self.match_key_list = []  # list(self.match_key.keys())

    def append_match(self, value, size):
        """
        更新搭配的次数，在原来的基础上增加或新增可搭配的品种
        :param value: 搭配的大品名
        :param size: 要更新的次数
        """
        if value in self.match_key:
            self.match_key[value] += size
        else:
            self.match_key[value] = size
            # self.match_key_list.append(value)

    # def update_match_order(self):
    #     self.match_key_list = []
    #     for key in self.match_key:
    #         self.match_key_list.append(key)

    def get_match_dic(self):
        """
        返回可搭配的货物字典
        :return:
        """
        return self.match_key

    def __str__(self):
        result = copy.deepcopy(self.main_key)
        result += ":"
        for i in self.match_key:
            result = result + i + "," + str(self.match_key[i])
            result += ";"
        return result
