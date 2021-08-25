from app.main.entity.batch import Batch

C = 100

class Hungarian_Algorithm:
    def __init__(self, batch: Batch):
        self.batch = Batch()
        self.u = len(self.batch.car_list)
        self.v = len(self.batch.can_be_sent_load_plan)
        self.used = [False for i in range(C)]
        self.g = [[False for i in range(C)] for i in range(C)]
        self.wm = [[0 for i in range(C)] for i in range(C)]
        self.linker = []

    def change_batch(self, batch: Batch):
        self.batch = batch
        self.u = len(self.batch.car_list)
        self.v = len(self.batch.can_be_sent_load_plan)
        self.clu_Connectivity()



    def clu_Connectivity(self):
        car_num = len(self.batch.car_list)
        if car_num == 0:
            print('what...')
        LP_num = len(self.batch.can_be_sent_load_plan)
        weight_matrix = [[False for i in range(LP_num)] for i in range(car_num)]
        wm = [[ 0 for i in range(LP_num)] for i in range(car_num)]
        for i in range(car_num):  # 计算二部图之间的权值
            for j in range(LP_num):
                lp_car_city_set = set()
                lp_car_city_set.add(self.batch.can_be_sent_load_plan[j].car.city)
                if self.cul_Jaccard_coefficient(self.batch.car_list[i].city_set, lp_car_city_set) == 0:
                    weight_matrix[i][j] = False
                    wm[i][j] = -1
                    continue
                else:
                    weight_matrix[i][j] = True
                    jacc = self.cul_Jaccard_coefficient(self.batch.car_list[i].commodity_set, self.batch.can_be_sent_load_plan[j].commodity_list)
                    if jacc == 0:
                        wm[i][j] = 0.1 * self.batch.can_be_sent_load_plan[j].priority
                    else:
                        wm[i][j] = jacc * self.batch.can_be_sent_load_plan[j].priority
        self.g = weight_matrix
        self.wm = wm


    def cul_Jaccard_coefficient(self, car_set: set, lp_set: set):
        intersec = car_set.intersection(lp_set)
        uni = car_set.union(lp_set)
        return len(intersec) / len(uni)


    def dfs(self,u:int):
        for v in range(self.v):
            if self.g[u][v] == True and self.used[v] == False:
                self.used[v] = True
                if self.linker[v] == -1 or self.dfs(self.linker[v]):
                    self.linker[v] = u
                    return True
        return False

    def hungary(self):
        res = 0
        self.linker = [-1 for i in range(self.v)]
        self.used = [False for i in range(self.v)]
        for u in range(self.u):
            if self.dfs(u):
                res += 1
        for i in range(len(self.linker)):
            if self.linker[i] < self.u and self.linker[i] >= 0:
                res += self.wm[self.linker[i]][i]
        return res, self.linker
