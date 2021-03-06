# -*- coding: utf-8 -*-

import traceback
import pymysql
from pymysql import MySQLError

from app.utils.db_pool import db_pool_ods


class BaseDao:
    """封装数据库操作基础类"""

    def select_one(self, sql, values=None):
        try:
            conn = db_pool_ods.connection()
            cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
            if values:
                cursor.execute(sql, values)
            else:
                cursor.execut(sql)
            return cursor.fetchone()
        except Exception as e:
            traceback.print_exc()
            raise MySQLError
        finally:
            cursor.close()
            conn.close()

    def select_all(self, sql, values=None):
        try:
            conn = db_pool_ods.connection()
            cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
            if values:
                cursor.execute(sql, values)
            else:
                cursor.execute(sql)
            return cursor.fetchall()
        except Exception as e:
            traceback.print_exc()
            raise MySQLError
        finally:
            cursor.close()
            conn.close()

    def execute(self, sql, values=None):
        try:
            conn = db_pool_ods.connection()
            cursor = conn.cursor()
            if values:
                cursor.execute(sql, values)
            else:
                cursor.execute(sql)
            conn.commit()
        except Exception as e:
            traceback.print_exc()
            conn.rollback()
            raise MySQLError
        finally:
            cursor.close()
            conn.close()

    def executemany(self, sql, values=None):
        try:
            conn = db_pool_ods.connection()
            cursor = conn.cursor()
            if values:
                cursor.executemany(sql, values)
            else:
                cursor.executemany(sql)
            conn.commit()
        except Exception as e:
            traceback.print_exc()
            conn.rollback()
            raise MySQLError
        finally:
            cursor.close()
            conn.close()
