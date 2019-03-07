#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
@Author: Jia_Xin
@Contact: 785415581@qq.com
@File: teacher_views.py
@Date: 2019/2/28 10:11
'''

from django.shortcuts import render,redirect


import pymysql

def teacher(request):

    conn = pymysql.connect(host = '127.0.0.1',port = 3306,user = 'root',password = 'root',db = 'django',charset = 'utf8')
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    cursor.execute("select id,name from teacher")
    teacher_list = cursor.fetchall()
    cursor.close()
    conn.close()

    return render(request,'teacher.html',{"teacher_list":teacher_list})

def add_teacher(request):

    if request.method == 'GET':


        return render(request,'add_teacher.html')

    else:
        # print(request.POST)
        v = request.POST.get('name')
        if len(v)>0:

            conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='root', db='django', charset='utf8')
            cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
            cursor.execute("insert into teacher(name) values(%s)",[v,])
            conn.commit()
            cursor.close()
            conn.close()
            return redirect('/teacher/')
        else:
            return render(request,'add_teacher.html',{'msg':'教师姓名不能为空'})



def edit_teacher(request):

    if request.method == "GET":

        nid = request.GET.get('nid')
        conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='root', db='django', charset='utf8')
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        cursor.execute("select name from teacher where id=%s", [nid, ])
        result = cursor.fetchone()
        cursor.close()
        conn.close()

        return render(request,'edit_teacher.html',{"result":result})
    else:
        nid = request.GET.get('nid')
        name = request.POST.get('name')
        conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='root', db='django', charset='utf8')
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        cursor.execute("update teacher set name=%s where id=%s", [name,nid, ])
        conn.commit()
        cursor.close()
        conn.close()

        return redirect('/teacher/')


def del_teacher(request):

    nid = request.GET.get('nid')

    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='root', db='django', charset='utf8')
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    cursor.execute("delete from teacher where id=%s", [nid, ])
    conn.commit()
    cursor.close()
    conn.close()

    return redirect('/teachers/')



