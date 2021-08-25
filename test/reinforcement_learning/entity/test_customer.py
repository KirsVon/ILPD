'''
    @Adaptive Dynamic Bipartite Graph Matching: A Reinforcement Learning Approach
    #基本客户类型包括客户的基本信息： 客户的id，客户的目前位置：x,y、要去的位置：des_x、des_y
'''
class test_customer:

    def __init__(self,id:int,loc_x:float,loc_y:float,des_x:float,des_y:float):
        self.cu_id = id
        self.cu_loc_x = loc_x
        self.cu_loc_y = loc_y
        self.cu_des_x = des_x
        self.cu_des_y = des_y