# @Time :  22:42

# @Author : Hu Yaoyi

# @File : distance.py

import requests
from math import radians, cos, sin, asin, sqrt


#申请的key,请大家自己申请哈，原来给了我的Ak，结果有人给我把一天的配额用完了
ak = '533b54ede4a766f33a8887eb0da28f0f'


#传入地址，返回对应地址的经纬度信息
def geocode(address):
    url = "https://restapi.amap.com/v3/geocode/geo?key=%s&address=%s"%(ak,address)
    data = requests.get(url)
    answer = data.json()
    lon = float(answer['geocodes'][0]['location'].split(',')[0])
    lat = float(answer['geocodes'][0]['location'].split(',')[1])
    return lon, lat

def get_distance(address1, address2):
    lon1, lat1 = geocode(address1)
    lon2, lat2 = geocode(address2)

    # 将十进制度数转化为弧度
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # haversine公式
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    r = 6371  # 地球平均半径，单位为公里
    return c * r * 1000

if __name__ == '__main__':
    address1 = '上海市中山北路3663号'
    address2 = '上海市青浦区泰禾红桥'

    print(get_distance(address1, address2))
