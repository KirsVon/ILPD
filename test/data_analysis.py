import pandas as pd
from datetime import timedelta, datetime

start_time = '20201016000000'
end_time = '20201024000000'

weight_list = []

while start_time <= end_time:
    df = pd.read_csv('C:/Users/93742/Desktop/experiment/result/PG/' + start_time + '.csv')
    weight = list(df['weight'])
    sumw = 0
    for i in weight:
        sumw += i
    weight_list.append(sumw)
    temp = datetime.strptime(start_time, '%Y%m%d%H%M%S')
    temp += timedelta(days=1)
    start_time = datetime.strftime(temp, '%Y%m%d%H%M%S')

print(weight_list)