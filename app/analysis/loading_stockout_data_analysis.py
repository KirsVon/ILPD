# -*- coding: utf-8 -*-
# Description:
# Created: Fengchong 2020/09/18
import json
import pandas as pd
import pymysql
from config import LocalConfig
import numpy as np



def get_DataFrame(db_name, cursor:pymysql.cursors.Cursor):
    sql = "select * from " + db_name
    cursor.execute(sql)
    data = cursor.fetchall()
    #下面将数据转化为dataframe格式
    columnDes = cursor.description
    columnNames = [columnDes[i][0] for i in range(len(columnDes))]
    df = pd.DataFrame([list(i) for i in data], columns = columnNames)
    return df

def DataPreprocessing(Df_one:pd.DataFrame, Df_two:pd.DataFrame):
    #预处理掉场内车辆
    df = pd.merge(Df_one,Df_two, how='left',on='main_produc')
    df_merge = df.dropna(subset=['commodity_n'])
    car_num = []
    for index, row in df_merge.iterrows():
        if row["carmark"][0] >= 'A' and row["carmark"][0] <= 'Z':
            car_num.append(index)
    df_merge.drop(index = car_num, inplace=True)
    print(len(df_merge))
    return df_merge

def get_Result(Df_one:pd.DataFrame, Df_two:pd.DataFrame):
    df = pd.merge(Df_one, Df_two, how='left', on=['create_time','carmark'])
    return df

def check_contain_chinese(check_str):
    for ch in check_str.decode('utf-8'):
          if u'\u4e00' <= ch <= u'\u9fff':
             return True
    return False

def DataFrame_to_sheet(df:pd.DataFrame):
    df.groupby(['carmark', 'create_time_x'])
    groups = df.groupby(['carmark', 'create_time_x'])
    sheet = pd.DataFrame(columns=['carmark', 'create_time', 'commodity_list', 'weight','per_weight'])
    dic = dict(groups.groups)
    carmark_list = []
    ct_list = []
    commodity_list = []
    weight_list = []
    per_catagory_list = []
    num = 0
    for kv in dic.items():
        print(num+1)
        num+=1
        carmark = kv[0][0]
        ct = kv[0][1]
        list_order = list(kv[1])
        carmark_list.append(carmark)
        ct_list.append(ct)
        c_list = []
        c_set = set()
        weight = 0
        weight_dic = {}
        count_dic = {}
        for i in range(len(list_order)):
            c_list.append(df.loc[list_order[i]]['commodity_n'])
            if df.loc[list_order[i]]['commodity_n'] not in c_set:
                c_set.add(df.loc[list_order[i]]['commodity_n'])
                weight_dic[df.loc[list_order[i]]['commodity_n']] = float(df.loc[list_order[i]]['weight'])
                count_dic[df.loc[list_order[i]]['commodity_n']] = int(df.loc[list_order[i]]['count'])
            else:
                tempweight = weight_dic[df.loc[list_order[i]]['commodity_n']]
                tempweight += float(df.loc[list_order[i]]['weight'])
                weight_dic[df.loc[list_order[i]]['commodity_n']] = tempweight
                tempcount = count_dic[df.loc[list_order[i]]['commodity_n']]
                tempcount += int(df.loc[list_order[i]]['count'])
                count_dic[df.loc[list_order[i]]['commodity_n']] = tempcount
            weight += float(df.loc[list_order[i]]['weight'])
        commodity_list.append(c_list)
        weight_list.append(weight)
        perweight = {}
        for item in weight_dic.items():
            k = item[0]
            v = item[1]
            if count_dic[k] == 0:
                perweight[k] = np.nan
            else:
                perweight[k] = v / count_dic[k]
        per_catagory_list.append(perweight)
    sheet['carmark'] = carmark_list
    sheet['create_time'] = ct_list
    sheet['commodity_list'] = commodity_list
    sheet['weight'] = weight_list
    sheet['per_weight'] = per_catagory_list
    return sheet

def str_to_list(s:str):
    l = len(s)
    i = 0
    set_list = set()
    while i < l - 1:
        st = s.find("'",i)
        ed = s.find("'",st + 1)
        tempstr = s[st + 1:ed]
        if tempstr not in set_list:
            set_list.add(tempstr)
        i = ed + 1
    return set_list


class Analysis:
    def get_loading_Stockout_comparation(self,zcoutputpath:str,ckoutputpath:str,zc_ckoutputpath:str,zckoutputpath:str):
        #出库装车清单比较
        pd.set_option('display.float_format', lambda x: '%.3f' % x)
        conn = pymysql.connect(
            host=LocalConfig.ODS_MYSQL_HOST,  # ip
            database=LocalConfig.ODS_MYSQL_DB,
            user=LocalConfig.ODS_MYSQL_USER,  # 用户名
            password=LocalConfig.ODS_MYSQL_PASSWD,  # 密码
            port=LocalConfig.ODS_MYSQL_PORT,  # 端口号
        )
        #装车清单

        cursor = conn.cursor()
        zc_main = get_DataFrame('stacking_main',cursor)
        zc_detail = get_DataFrame('stacking_detail',cursor)
        df_zc = DataPreprocessing(zc_main,zc_detail)
        zc_sheet = DataFrame_to_sheet(df_zc)
        outputp = zcoutputpath
        zc_sheet.to_csv(outputp,sep=',',index=False,header=True,encoding='UTF-8')
        print("Well")

        #出库清单
        ck_main = get_DataFrame('ods_db_inter_bclp_bill_of_loading_no_main',cursor)
        ck_detail = get_DataFrame('ods_db_inter_bclp_bill_of_loading_no_detail',cursor)
        df_ck = DataPreprocessing(ck_main, ck_detail)
        ck_sheet = DataFrame_to_sheet(df_ck)
        print(ck_sheet)
        outputpath = ckoutputpath
        ck_sheet.to_csv(outputpath,sep=',',index=False,header=True,encoding='UTF-8')
        print("Well Well...")

        ck_sheet.to_csv(outputpath, sep=',',index=False,header=True)
        zc_ck = get_Result(zc_sheet,ck_sheet)
        print(zc_ck)
        output = zc_ckoutputpath
        zc_ck.to_csv(output,sep=',',index=False,header=True,encoding='UTF-8')
        zck = zc_ck.dropna(subset=['commodity_list_y'])
        output = zckoutputpath
        zck.to_csv(output,sep=',',index=False,header=True)
        print("Finish")
    def Type_Matching_Analysis(self,filepath):
        #出库商品类目/装车商品类目差异
        df = pd.read_csv(filepath)
        zc_list = df[['commodity_list_x','weight_x']]
        ck_list = df[['commodity_list_y','weight_y']]
        zc_type = zc_list['commodity_list_x']
        zc_weight = zc_list['weight_x'].tolist()
        ck_type = ck_list['commodity_list_y']
        ck_weight = ck_list['weight_y'].tolist()
        difference_list = []
        difference_setlist = []
        for i in range(0,len(zc_list)):
            set_a = str_to_list(zc_list.iloc[[i]]['commodity_list_x'].values[0])
            set_b = str_to_list(ck_list.iloc[[i]]['commodity_list_y'].values[0])
            a_d_b = set_a.difference(set_b)
            b_d_a = set_b.difference(set_a)
            difference_list.append(a_d_b)
            difference_setlist.append(b_d_a)
        count = 0
        for i in range(0, len(difference_setlist)):
            if len(difference_setlist[i]) != 0:
                count += 1
        print("差异率：", count/(len(difference_setlist)))
        print(difference_setlist)
        Digitial_Difference = []
        for i in range(0, len(ck_weight)):
            Digitial_Difference.append(ck_weight[i] - zc_weight[i])
if __name__ == '__main__':
    a = Analysis()
    a.Type_Matching_Analysis('C:/Users/FC/Desktop/zck.csv')
    # a.get_loading_Stockout_comparation()



