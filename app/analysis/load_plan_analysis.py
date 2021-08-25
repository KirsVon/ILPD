# -*- coding: utf-8 -*-
# Description:
# Created: liujiaye  2019/12/21
import json
from app.main.entity.car import Car
from config import config
from app.main.controller.config_name_management import curr_config_class
import pymysql
from _datetime import datetime
from app.tool.priority_ratio_calculation import priority_ratio_calculate_by_list

# read data from db, transform load_plan *2(this & result)
# analysis ,weight\count,
# display


def read_trucks(file_name):
    # basedir = os.path.abspath(os.path.dirname(__file__))
    file_path = "F:\\github\\Dispatch-of-Goods\\test\\json_data\\" + file_name
    trucks = []
    # , encoding = 'utf-8'
    with open(file_path, 'r', encoding='utf-8') as load_f:
        cars = json.load(load_f)
    for c in cars:
        c['license_plate_number'] = c['car_mark']
        c['district'] = c['end_point']
        c['load_capacity'] = c['weight']
        tmp_truck = Car(c)
        trucks.append(tmp_truck)
    return trucks


class Experiment:
    def __init__(self):
        self.truck_dic = {}  # "car_mark+arrive_time":Car
        self.load_plan_priority = {}  # id:[opt,his,greedy,gentic,fixw,adpw]
        self.response_time = {}  # id:[fix,adpw]

    def init_truck(self, truck_list):
        for i in truck_list:
            key = i.license_plate_number + "," + i.arrive_time.strftime("%Y-%m-%d %H:%M:%S")
            self.truck_dic[key] = i
            self.load_plan_priority[key] = {"opt": 0.0, "greedy": 0.0, "gentic": 0.0, "fixw": 0.0, "adpw": 0.0}
            self.response_time[key] = {"fixw": 0, "adpw": 0}

    def get_experiment_result(self):
        if len(self.truck_dic) <= 0:
            print("truck not initialize")
            return False

        conn = pymysql.connect(
            host=config[curr_config_class].host_db,  # ip
            database=config[curr_config_class].database_allocation,
            user=config[curr_config_class].user_db,  # 用户名
            password=config[curr_config_class].password_db,  # 密码
            port=config[curr_config_class].port_db,  # 端口号
        )
        cursor = conn.cursor()
        # opt
        sql = "select * from loading_task_main_opt"
        cursor.execute(sql)
        lines = cursor.fetchall()
        for row in lines:
            if row[2] + "," + row[15] in self.truck_dic:
                self.load_plan_priority[row[2] + "," + row[15]]["opt"] = float(row[9])
            else:
                print("1 error entity:" + row[2] + "," + row[15])

        # his
        # greedy
        sql = "select * from vt_load_plan_greedy_result"
        cursor.execute(sql)
        lines = cursor.fetchall()
        weight_dic = {}
        for row in lines:
            arrive_date = datetime.strptime(row[1], "%Y%m%d%H%M%S")
            differ = 105 - (arrive_date.day - 3)
            time_str = arrive_date.strftime("%Y-%m-%d %H:%M:%S")
            key = row[0] + "," + time_str
            if key not in weight_dic:
                weight_dic[key] = []
            else:
                weight_dic[key].append([float(row[2]), int(row[3]) - differ])
        for key in weight_dic:
            if key in self.truck_dic:
                self.load_plan_priority[key]["greedy"] = priority_ratio_calculate_by_list(weight_dic[key])
            else:
                print("greedy error entity:" + key)

        # gentic
        sql = "select * from loading_task_main_gentic"
        cursor.execute(sql)
        lines = cursor.fetchall()
        for row in lines:
            if row[2] + "," + row[15] in self.truck_dic:
                self.load_plan_priority[row[2] + "," + row[15]]["gentic"] = float(row[9])
        else:
            print("2 error entity:" + row[2] + "," + row[15])
        # fixw
        sql = "select * from loading_task_main_fixw"
        cursor.execute(sql)
        lines = cursor.fetchall()
        for row in lines:
            if row[2] + "," + row[15] in self.truck_dic:
                self.load_plan_priority[row[2] + "," + row[15]]["fixw"] = float(row[9])
                response_time = (datetime.strptime(row[7], "%Y-%m-%d %H:%M:%S") - datetime.strptime(row[15],
                                                                                                    "%Y-%m-%d %H:%M:%S")).seconds
                self.response_time[row[2] + "," + row[15]]["fixw"] = response_time
            else:
                print("3 error entity:" + row[2] + "," + row[15])
        # adpw
        sql = "select * from loading_task_main_adpw"
        cursor.execute(sql)
        lines = cursor.fetchall()
        for row in lines:
            if row[2] + "," + row[15] in self.truck_dic:
                self.load_plan_priority[row[2] + "," + row[15]]["adpw"] = float(row[9])
                response_time = (datetime.strptime(row[7], "%Y-%m-%d %H:%M:%S") - datetime.strptime(row[15],
                                                                                                    "%Y-%m-%d %H:%M:%S")).seconds
                self.response_time[row[2] + "," + row[15]]["adpw"] = response_time
            else:
                print("4 error entity:" + row[2] + "," + row[15])
        conn.close()

    def write_result(self):
        fp = open("result_priority.txt",'w')
        fr = open("result_response.txt",'w')
        for key in self.truck_dic:
            if self.load_plan_priority[key]['adpw']==0.0:
                continue
            fp.write(str(key))
            fp_line = ""
            for i in self.load_plan_priority[key]:
                fp_line = fp_line + "," + str(self.load_plan_priority[key][i])
            fp.write(fp_line + "\n")

            fr.write(str(key))
            fr_line = ""
            for i in self.response_time[key]:
                fr_line = fr_line + "," + str(self.response_time[key][i])
            fr.write(fr_line + "\n")
        fp.close()
        fr.close()


if __name__ == '__main__':
    truck_list = []
    truck_list.extend(read_trucks("0704.json"))
    truck_list.extend(read_trucks("0705.json"))
    truck_list.extend(read_trucks("0706.json"))
    e = Experiment()
    e.init_truck(truck_list)
    print(len(e.truck_dic))
    e.get_experiment_result()
    print("start to write")
    e.write_result()
