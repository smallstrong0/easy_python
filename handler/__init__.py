#! /usr/bin/env python
# -*- coding: utf-8 -*-

# @Author: ss
# @Time: 2020/7/17 11:45 上午
# @File: __init__.py.py
import concurrent.futures
import time
from concurrent.futures import ThreadPoolExecutor

from apscheduler.executors import tornado
import tornado
import threading
import asyncio

new_loop = asyncio.new_event_loop()
asyncio.set_event_loop(new_loop)
ylc_thread_pool = concurrent.futures.ThreadPoolExecutor(
    thread_name_prefix='ylc',
    max_workers=10
)


class ServiceThreadPoolExecutor(ThreadPoolExecutor):

    def __init__(self, max_workers=None, thread_name_prefix='',
                 initializer=None, initargs=()):

        ThreadPoolExecutor.__init__(self, max_workers=max_workers, thread_name_prefix=thread_name_prefix,
                                    initializer=None, initargs=())


    def async_exec(self,*args,**kwargs):
        asyncio.set_event_loop()
        try:
            keys = kwargs
            print('async_exec {}'.format(threading.current_thread().name))
            # tornado.ioloop.IOLoop.current().run_in_executor(self, self.do_task, *args,**kwargs)
            if len(args)>1:
                tornado.ioloop.IOLoop.current().run_in_executor(self, self.do_task, *args ,keys)
            else:
                tornado.ioloop.IOLoop.current().run_in_executor(self, self.do_task,args[0],None, keys)
        except Exception as e:
            print(e)
            pass


    def do_task(self,fun, *args,**kwargs):
        # args = *args
        try:
            print('1do_task {}'.format(threading.current_thread().name))
            arg=[]
            kwarg={}
            for index in range(len(args)):
                if index+1 < int(len(args)):
                    arg.append(args[index])
                else:
                    kwarg=args[int(len(args))-1]

            if arg is None or (len(arg)==1 and arg[0] is None):
                fun(**kwarg)
            else:
                fun(*arg,**kwarg)
            print('2do_task {}'.format(threading.current_thread().name))
        except Exception as e:
            pass


service_thread_pool = ServiceThreadPoolExecutor(
    thread_name_prefix='service',
    max_workers=3
)
