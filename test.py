#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
@Author: Jia_Xin
@Contact: 785415581@qq.com
@File: test.py
@Date: 2019/3/2 16:43
'''

#
# v = [
#         {'title': 'Python研发2班', 'tid': 1, 'name': '秦家鑫'},
#          {'title': 'Python研发3班', 'tid': 1, 'name': '秦家鑫'},
#          {'title': 'Python研发2班', 'tid': 3, 'name': '韦斯特'},
#          {'title': 'Python研发3班', 'tid': 3, 'name': '韦斯特'},
#          {'title': 'Python研发4班', 'tid': 4, 'name': '布鲁斯'},
#          {'title': 'Python研发3班', 'tid': 4, 'name': '布鲁斯'},
#          {'title': 'Python研发2班', 'tid': 5, 'name': '梅卡多'}
#      ]
# result = {}
#
# for row in v:
#     tid = row['tid']
#     if tid in result:
#         result[tid]['titles'].append(row['title'])
#     else:
#         result[tid] = {'tid':row['tid'],'name':row['name'],'titles':[row['title'],]}
#
# for item in result.values():
#     print(item)


# import sys
# import time
# from math import sqrt
#
# PW = 5209527
#
#
# def is_prime(n):
#     for i in range(3, int(sqrt(n)) + 2, 2):
#         if n % i == 0:
#             return False
#     return True
#
#
# class ProgressBar:
#     def __init__(self, total=0, width=20):
#         self.total = total
#         self.width = width
#
#     def show(self, count, done='#', wait='-'):
#         proc = self.width * count // self.total
#         ok, undo = done * proc, wait * (self.width - proc)
#         print(f'\rRunning... [{ok}{undo}] {count}/{self.total}', end='')
#
#
# def main(total=PW):
#     start = time.time()
#     n = 3
#     bar = ProgressBar(total)
#     for p in range(2, total):
#         while True:
#             n += 2
#             if is_prime(n):
#                 bar.show(p + 1)
#                 break
#
#     end = time.time()
#     print(f'\ncost: {end-start} sec, result: {n}')
#
# if __name__ == '__main__':
#     main()



# from utils import sqlheper
#
# teacher_name = '秦家鑫外部创w建'
# techer_id= sqlheper.create('insert into teacher(name) values(%s)',[teacher_name,])
#
#
# print(techer_id)






def say_goodbye():

    print('goodbye')


def say_helloAndgoodbye(func):
    def wrapper():
        print('hello_goodbye')
        return func()
    return wrapper







def logging(level):
    def wrapper(func):
        def inner_wrapper(*args, **kwargs):
            print("[{level}]: enter function {func}()".format(
                level=level,
                func=func.__name__))
            return func(*args, **kwargs)
        return inner_wrapper
    return wrapper


@logging(level='INFO')

def say(something):
    print("say {}!".format(something))



def make_printer(msg1, msg2):
    def printer():
        print(msg1, msg2)
    return printer


printer = make_printer('foo','msg')

def logging(level):
    def wrapper(func):
        def inner_wrapper(*args, **kwargs):
            print("[{level}]: enter function {func}()".format(
                level=level,
                func=func.__name__))
            return func(*args, **kwargs)
        return inner_wrapper
    return wrapper

@logging(level='INFO')
def say(something):
    print("say {}!".format(something))

# 如果没有使用@语法，等同于
# say = logging(level='INFO')(say)

@logging(level='DEBUG')
def do(something):
    print("do {}...".format(something))



def say_hello():
    print('hello')

say_hello()

































