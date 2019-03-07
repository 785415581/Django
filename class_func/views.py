#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
@Author: Jia_Xin
@Contact: 785415581@qq.com
@File: views.py
@Date: 2019/2/27 12:05
'''

from django.shortcuts import render,redirect,HttpResponse
import pymysql
from utils import sqlheper

import json





def auth(func):
    def inner(request,*args,**kwargs):
        v = request.COOKIES.get('ticket')
        if not v:
            return redirect('/login')
        return func(request,*args,**kwargs)
    return inner


@auth
def classes(request):


    conn = pymysql.connect(host = '127.0.0.1',port = 3306,user = 'root',password = 'root',db = 'django',charset = 'utf8')
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    cursor.execute("select id,title from class")
    class_list = cursor.fetchall()
    cursor.close()
    conn.close()

    return render(request,'classes.html',{'class_list':class_list})


@auth
def add_class(request):




    if request.method == 'GET':

        return render(request,'add_classes.html')

    else:
        v = request.POST.get('title')

        if len(v)>0:
            conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='root', db='django', charset='utf8')
            cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
            cursor.execute("insert into class(title) values(%s)",[v,])
            conn.commit()
            cursor.close()
            conn.close()

            # return render(request,'classes.html')
            return redirect('/classes/')
        else:
            return render(request,'add_classes.html',{'msg':"班级名称不能为空"})
@auth
def edit_class(request):

    if request.method == 'GET':

        nid = request.GET.get('nid')
        conn = pymysql.connect(host='127.0.0.1', port=3306,  user='root', password='root', db='django', charset='utf8')
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        cursor.execute("select id,title from class where id=%s", [nid, ])
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return render(request,'edit_class.html',{"result":result})

    else:

        nid = request.GET.get('nid')
        title = request.POST.get('title')
        conn = pymysql.connect(host='127.0.0.1', port=3306,  user='root', password='root', db='django', charset='utf8')
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        cursor.execute("update class set title=%s where id=%s", [title,nid,])
        conn.commit()
        cursor.close()
        conn.close()
        return redirect('/classes/')

@auth
def edit_modal_class(request):

    ret = {'status':True,'message':None}
    try:
        nid = request.POST.get('nid')
        content = request.POST.get('content')
        print(nid,content)
        sqlheper.modify('update class set title=%s where id=%s',[content,nid,])
    except Exception as e:
        ret['status'] = False
        ret['message'] = '处理异常'
    return HttpResponse(json.dumps(ret))

@auth
def del_class(request):


    nid = request.GET.get('nid')
    sqlheper.modify("delete from class where id=%s", [nid, ])
    return HttpResponse('ok')

@auth
def modal_add_class(request):
    title = request.POST.get('title')
    print(title)

    if len(title)>0:
        sqlheper.modify('insert into class(title) values(%s)',[title,])
        return HttpResponse('ok')
    else:
        return HttpResponse('班级信息不能为空')

@auth
def teachers(request):

    teacher_list = sqlheper.get_list("""select teacher.id as tid,teacher.name,class.title from teacher
                                        left join teacher2class on teacher.id = teacher2class.teacher_id
                                        LEFT join class on class.id = teacher2class.class_id;
                                      """,[])
    # print(teacher_list)

    result = {}

    for row in teacher_list:
        tid = row['tid']
        if tid in result:
            result[tid]['titles'].append(row['title'])
        else:
            result[tid] = {'tid': row['tid'], 'name': row['name'], 'titles': [row['title'], ]}

    return render(request,'teacher.html',{'teacher_list':result.values()})

@auth
def add_teacher(request):

    if request.method == "GET":
        class_list = sqlheper.get_list('select * from class',[])
        return render(request,'add_teacher.html',{'class_list':class_list})

    else:
        name = request.POST.get('name')
        class_ids = request.POST.getlist('class_ids')
        teacher_id = sqlheper.create('insert into teacher(name) values(%s)',[name,])

        #多次链接多次提交
        # for cls_id in class_ids:
        #     sqlheper.modify('insert into teacher2class (teacher_id,class_id) values (%s,%s)',[teacher_id,cls_id,])

        # 一次链接多次提交
        # obj = sqlheper.Sqlheper()
        # for cls_id in class_ids:
        #     obj.modify('insert into teacher2class (teacher_id,class_id) values (%s,%s)',[teacher_id,cls_id,])
        # obj.close()

        #一次链接一次提交
        data_list = []
        for cls_id in class_ids:
            temp = (teacher_id,cls_id,)
            data_list.append(temp)
        obj = sqlheper.Sqlheper()
        obj.multiple_modify('insert into teacher2class (teacher_id,class_id) values (%s,%s)',data_list)
        obj.close()


        return redirect('/teachers/')

@auth
def edit_teacher(request):


    if request.method == 'GET':

        nid = request.GET.get('nid')
        obj = sqlheper.Sqlheper()
        teacher_info = obj.get_one('select id,name from teacher where id = %s',[nid])
        class_id_list = obj.get_list('select teacher_id,class_id from teacher2class where teacher_id=%s',[nid,])
        class_list = obj.get_list('select id,title from class',[])
        obj.close()

        temp = []
        for i in class_id_list:
            temp.append(i['class_id'])


        return render(request,'edit_teacher.html',{
            'teacher_info':teacher_info,
            'class_id_list':temp,
            'class_list':class_list,
        })

    else:

        nid = request.GET.get('nid')
        name = request.POST.get('name')
        class_ids = request.POST.getlist('class_id')

        obj = sqlheper.Sqlheper()
        #更新老师表
        obj.modify('update teacher set name=%s where id=%s',[name,nid,])
        #更新老师和班级关系表
        #先把当前老师和班级的对应关系删除，然后再添加
        obj.modify('delete from teacher2class where teacher_id=%s',[nid,])
        data_list = []
        for cls_id in class_ids:
            temp = (nid,cls_id,)
            data_list.append(temp)

        obj = sqlheper.Sqlheper()
        obj.multiple_modify('insert into teacher2class (teacher_id,class_id) values (%s,%s)',data_list)
        obj.close()
        return redirect('/teachers/')


@auth
def get_all_class(request):

    obj = sqlheper.Sqlheper()
    class_list = obj.get_list('select id,title from class',[])
    obj.close()

    return HttpResponse(json.dumps(class_list))

@auth
def modal_add_teacher(request):


    ret = True

    try:
        name = request.POST.get('name')
        if name == '':
            ret = False
        else:
            class_id_list = request.POST.getlist('class_id_list')
            teacher_id = sqlheper.create('insert into teacher(name) values(%s)', [name, ])
            # class_ids = request.POST.getlist('class_ids')
            print(name,class_id_list)
            data_list = []
            for cls_id in class_id_list:
                temp = (teacher_id, cls_id,)
                data_list.append(temp)
            obj = sqlheper.Sqlheper()
            obj.multiple_modify('insert into teacher2class (teacher_id,class_id) values (%s,%s)', data_list)
            obj.close()

    except Exception as e:
        ret = False

    return HttpResponse(json.dumps(ret))


@auth
def transfrom_edit_teacher(request):


    if request.method == 'GET':

        nid = request.GET.get('nid')
        obj = sqlheper.Sqlheper()
        teacher_info = obj.get_one('select id,name from teacher where id = %s',[nid])
        class_id_list = obj.get_list('select teacher_id,class_id from teacher2class where teacher_id=%s',[nid,])
        class_list = obj.get_list('select id,title from class',[])
        obj.close()

        temp = []
        for i in class_id_list:
            temp.append(i['class_id'])


        return render(request,'transfrom_edit_teacher.html',{
            'teacher_info':teacher_info,
            'class_id_list':temp,
            'class_list':class_list,
        })

@auth
def rightToleft(request):



    select_class_id_list = request.POST.getlist('select_class_id_list')

    obj = sqlheper.Sqlheper()
    class_id = []
    for i in select_class_id_list:
        class_name = obj.get_list('select id,title from class where id=%s',[i,])
        class_id.append(class_name[0])
    obj.close()
    print(class_id)

    return HttpResponse(json.dumps(class_id))


    # return render(request,'transfrom_edit_teacher.html',{'class_id':class_id})

@auth
def leftToright(request):




    class_id = request.POST.getlist('select_class_id_list')

    obj = sqlheper.Sqlheper()

    class_list = []

    for i in class_id:
        class_name = obj.get_list('select id,title from class where id=%s',[i,])
        class_list.append(class_name[0])
    obj.close()

    print(class_list)
    return HttpResponse(json.dumps(class_list))



def login(request):

    if request.method == 'GET':
        return render(request,'login.html')
    else:
        user = request.POST.get('username')
        pwd = request.POST.get('password')
        if user == 'qinjiaxin' and pwd == '123':
            obj = redirect('/classes/')
            obj.set_cookie('ticket','asdasdasfasd')
            return obj
        else:
             return render(request,'login.html')



@auth
def layout(request):

    print(request)
    return render(request,'layout.html')





































































