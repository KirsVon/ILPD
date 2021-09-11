#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：ILPD 
@File    ：PG_Test.py
@IDE     ：PyCharm 
@Author  ：fengchong
@Date    ：2021/9/11 7:16 下午 
'''

from app.main.models.perturbed_greedy import Perturbed_Greedy

PG = Perturbed_Greedy('20201009000000', '20201010000000')

PG.pertubed_greedy_matching()