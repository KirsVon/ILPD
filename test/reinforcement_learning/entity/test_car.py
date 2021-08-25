'''
    @Adaptive Dynamic Bipartite Graph Matching: A Reinforcement Learning Approach
    #基本车类型包括车的基本信息： 车的id，车的目前位置：x,y
'''
class test_car:

    def __init__(self,id:int,loc_x:float,loc_y:float):
        self.car_id = id
        self.car_loc_x = loc_x
        self.car_loc_y = loc_y