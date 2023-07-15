#! /usr/bin/env python
# -*- coding: utf-8 -*-

# @Author: ss
# @Time: 2023-07-11 16:06:08
# @File: test.py

import lib.dao.test
import lib.common.const as com_const
import lib.common.error as error_const
import lib.common.func as com_func
from lib.model.model import Test
from lib.common.error import TestErrorType, CommonError
import lib.dao.sequence
from handler import ylc_thread_pool, service_thread_pool
from lib.common.aliyun_mysql import mysql_rds
from tornado.ioloop import IOLoop
import asyncio
# from aiohttp import ClientSession
import time
import threading
import aiohttp


def add_test(params):
    ts = com_func.get_ts()
    user_id = params['user_id']
    obj = Test(
        ctime=ts,
        mtime=ts,
        create_by=user_id,
        update_by=user_id
    )
    lib.dao.test.add_test(obj=obj)
    return None, {}


def bulk_add_test(params):
    ts = com_func.get_ts()
    user_id = params['user_id']
    info_list = params['info_list']
    data_list = []
    for info in info_list:
        data_list.append(
            {
                'ctime': ts,
                'mtime': ts,
                'create_by': user_id,
                'update_by': user_id,
            }
        )
    lib.dao.test.bulk_add_test(data_list=data_list)
    return None, {}


def update_test(params):
    ts = com_func.get_ts()
    user_id = params['user_id']
    test_id = params['test_id']
    data_dict = {
        'mtime': ts,
        'update_by': user_id
    }
    lib.dao.test.update_test(
        test_id=test_id,
        data_dict=data_dict
    )
    return None, {}


def delete_test(params):
    test_id = params['test_id']
    lib.dao.test.delete_test(test_id=test_id)
    return None, {}


async def get_res():
    url = 'http://www.baidu.com'
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            # await asyncio.sleep(2)
            res = await resp.text()
    return res


async def get_test(params):
    print('get_test {}'.format(threading.current_thread().name))
    print('start is {}'.format(com_func.get_ts()))
    session = mysql_rds.get_session()
    print(id(session))
    res = await get_res()
    return None, {
        'msg': res
    }


def get_test_list(params):
    page = int(params['page'])
    pagesize = int(params['pagesize'])
    data_list = lib.dao.test.get_test_list(
        page=page,
        pagesize=pagesize
    )
    count = lib.dao.test.get_test_list_count()
    result = com_func.pagination(
        data_list, count, page, pagesize
    )
    return None, result
