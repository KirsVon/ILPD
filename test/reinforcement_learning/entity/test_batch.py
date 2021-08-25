'''
    @Adaptive Dynamic Bipartite Graph Matching: A Reinforcement Learning Approach
    #基础批：包含批中左右节点的车的节点数、顾客的节点数、以及基本信息
'''
from test.reinforcement_learning.entity.test_car import test_car
from test.reinforcement_learning.entity.test_customer import test_customer

class test_batch:
    def  __init__(self):
        self.carlist = []
        self.customerlist = []

    def  insert_car(self,car:test_car):
        self.carlist.append(car)

    def  insert_customer(self,customer:test_customer):
        self.customerlist.append(customer)
