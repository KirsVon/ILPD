# -*- coding: utf-8 -*-
# Description:
# Created: liujiaye  2020/07/23
from app.utils.base_dao import BaseDao
from datetime import datetime, timedelta
import pandas as pd
from sqlalchemy import create_engine


class DataOutFile(BaseDao):

    def output_file(self, start_time_str, end_time_str, interval):
        start_time = datetime.strptime(start_time_str, "%Y-%m-%d %H:%M:%S.%f")
        end_time = datetime.strptime(end_time_str, "%Y-%m-%d %H:%M:%S.%f")
        current = start_time + timedelta(minutes=interval)  # microseconds
        print("begin loop")
        while current < end_time:
            self.output_one(start_time.strftime("%Y-%m-%d %H:%M:%S.%f"), current.strftime("%Y-%m-%d %H:%M:%S.%f"))
            start_time = current + timedelta(microseconds=1)
            current = current + timedelta(minutes=interval)
            print(current.strftime("%Y-%m-%d %H:%M:%S.%f"))

    def output_one(self, start_time, end_time):
        sql = "select * from ods_db_inter_bclp_can_be_send_amount_log " \
              "where ods_update_time between '{0}' and '{1}'".format(start_time, end_time)
        # print(sql)
        df = pd.DataFrame(list(self.select_all(sql)))
        engine = create_engine('mysql+pymysql://root:liujiaye@localhost/jingchuang?charset=utf8')
        # df.to_csv(file_name, sep=',', header=True, index=True)
        df.to_sql('ods_db_inter_bclp_can_be_send_amount_log', engine, index=False, if_exists='append')
        # print(end_time)


if __name__ == '__main__':
    data_out_file = DataOutFile()
    data_out_file.output_file('2020-07-17 11:42:40.001', '2020-07-20 12:00:00.000', 1)
