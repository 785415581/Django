#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
@Author: Jia_Xin
@Contact: 785415581@qq.com
@File: student_views.py
@Date: 2019/2/28 13:25
'''


from django.shortcuts import redirect,render,HttpResponse
from utils import sqlheper
import pymysql
import json


def student(request):

    conn = pymysql.connect(host = '127.0.0.1',port = 3306,user = 'root',password = 'root',db = 'django',charset = 'utf8')
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    cursor.execute("select student.id,student.name,student.class_id,class.title from student left join class on student.class_id = class.id")
    student_list = cursor.fetchall()
    cursor.close()
    conn.close()
    class_list = sqlheper.get_list('select id,title from class',[])


    return render(request,'student/student.html',{'student_list':student_list,'class_list':class_list})


def add_student(request):

    if request.method == 'GET':
        conn = pymysql.connect(host = '127.0.0.1',port = 3306,user = 'root',password = 'root',db = 'django',charset = 'utf8')
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        cursor.execute("select id,title from class")
        class_list = cursor.fetchall()
        cursor.close()
        conn.close()
        return render(request,'student/add_student.html',{'class_list':class_list})

    else:

        class_id = request.POST.get('class_id')
        name = request.POST.get('name')

        if len(name)>0:

            conn = pymysql.connect(host = '127.0.0.1',port = 3306,user = 'root',password = 'root',db = 'django',charset = 'utf8')
            cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
            cursor.execute("insert into student(name,class_id) values(%s,%s)",[name,class_id,])
            conn.commit()
            cursor.close()
            conn.close()
            return redirect('/student/')

        else:
            return render(request,'student/add_student.html',{'msg':'学生姓名不能为空'})

def edit_student(request):

    if request.method == 'GET':
        nid = request.GET.get('nid')
        class_list = sqlheper.get_list('select id,title from class',[])
        current_student_info = sqlheper.get_one('select id,name,class_id from student where id=%s',[nid,])
        return render(request,'student/edit_student.html',{'class_list':class_list,'current_student_info':current_student_info})

    else:
        nid = request.GET.get('nid')
        name = request.POST.get('name')
        class_id = request.POST.get('class_id')
        sqlheper.modify('update student set name=%s,class_id=%s where id=%s',[name,class_id,nid])
        return redirect('/student/')



def modal_add_student(request):

    ret = {'status':True,'message':None}
    try:
        name = request.POST.get('name')
        class_id = request.POST.get('class_id')
        sqlheper.modify('insert into student(name,class_id) values(%s,%s)',[name,class_id,])
    except Exception as e:
        ret['status'] = False
        ret['message'] = str(e)


    return HttpResponse(json.dumps(ret))


def modal_edit_student(request):

    ret = {"status":True,"message":None}

    try:

        nid = request.POST.get('nid')
        name = request.POST.get('name')
        class_id = request.POST.get('class_id')
        sqlheper.modify('update student set name=%s,class_id=%s where id=%s',[name,class_id,nid])
        print(name,class_id,nid)

    except Exception as e:

        ret['status'] = False
        ret['message'] = str(e)

    return HttpResponse(json.dumps(ret))


def modal_del_student(request):

    ret = {"status":True,"message":None}

    try:
        id = request.POST.get('id')
        print(id)
        sqlheper.modify('delete from student where id=%s',[id,])

    except Exception as e:

        ret['status'] = False
        ret['message'] = str(e)

    return HttpResponse(json.dumps(ret))
















