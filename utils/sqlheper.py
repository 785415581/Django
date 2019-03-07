#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
@Author: Jia_Xin
@Contact: 785415581@qq.com
@File: sqlheper.py
@Date: 2019/2/28 14:39
'''

import pymysql


def get_list(sql,args):

    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='root', db='django', charset='utf8')
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    cursor.execute(sql,args)
    result = cursor.fetchall()
    cursor.close()
    conn.close()

    return result

def modify(sql,args):

    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='root', db='django', charset='utf8')
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    cursor.execute(sql,args)
    conn.commit()
    cursor.close()
    conn.close()

def get_one(sql,args):

    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='root', db='django', charset='utf8')
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    cursor.execute(sql,args)
    result = cursor.fetchone()
    cursor.close()
    conn.close()

    return result

def create(sql,args):

    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='root', db='django', charset='utf8')
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    cursor.execute(sql,args)
    last_id = conn.insert_id()
    conn.commit()
    cursor.close()
    conn.close()
    return last_id



class Sqlheper(object):
    '''
        可以配置数据库名称
        配置文件读取



    '''
    def __init__(self):
        self.connect()


    def connect(self):
        self.conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='root', db='django', charset='utf8')
        self.cursor = self.conn.cursor(cursor=pymysql.cursors.DictCursor)

    def get_list(self,sql,args):
        self.cursor.execute(sql, args)
        result = self.cursor.fetchall()

        return result

    def get_one(self,sql,args):
        self.cursor.execute(sql, args)
        result = self.cursor.fetchone()

        return result

    def modify(self,sql,args):
        self.cursor.execute(sql, args)
        self.conn.commit()

    def multiple_modify(self,sql,args):
        self.cursor.executemany(sql, args)
        self.conn.commit()


    def create(self,sql,args):
        self.cursor.execute(sql, args)
        self.conn.commit()

    def close(self):

        self.cursor.close()
        self.conn.close()


