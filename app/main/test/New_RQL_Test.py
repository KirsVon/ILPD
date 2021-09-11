from app.main.models.JC_QL import JC_QL
from app.main.models.entity.environment import Environment


JC_Test = JC_QL()
JC_Test.env_load_q_table('/./data/FC/experiment/0908/20201009000000.csv')

# JC_Test.env_load_q_table('/Users/lalala/Desktop/experiment/data/20201009000000.csv')
JC_Test.train_by_day(20)
