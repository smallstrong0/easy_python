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
from handler import ylc_thread_pool
from lib.common.aliyun_mysql import mysql_rds
from tornado.ioloop import IOLoop
import asyncio
# from aiohttp import ClientSession
import time
import threading
import aiohttp


async def add_test(params):
    ts = com_func.get_ts()
    user_id = 1
    obj = Test(
        ctime=ts,
        mtime=ts,
        create_by=user_id,
        update_by=user_id
    )
    await lib.dao.test.add_test(obj=obj)
    return None, {}


async def bulk_add_test(params):
    ts = com_func.get_ts()
    user_id = 1
    info_list = [1,2,3]
    data_list = []
    for info in info_list:
        data_list.append(
            Test(
                ctime=ts,
                mtime=ts,
                create_by=user_id,
                update_by=user_id
            )
        )
    await lib.dao.test.bulk_add_test(data_list=data_list)
    return None, {}


async def update_test(params):
    ts = com_func.get_ts()
    test_id = 1
    data_dict = {
        'mtime': 10086,
        'update_by': 10086
    }
    await lib.dao.test.update_test(
        test_id=test_id,
        data_dict=data_dict
    )
    return None, {}

async def bulk_update_test(params):
    ts = com_func.get_ts()
    test_id = 1
    await lib.dao.test.bulk_update_test(
        data_list=[
            {
                'test_id':1,
                'ctime':999
            },
            {
                'test_id': 3,
                'ctime': 777
            },
        ]
    )
    return None, {}


async def delete_test(params):
    test_id = 2
    await lib.dao.test.delete_test(test_id=test_id)
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
    data = await lib.dao.test.get_test(test_id=1)
    # res = await get_res()
    return None, {
        'msg': data
    }

async def get_all_test(params):
    data = await lib.dao.test.get_test_list_all()
    return None, {
        'msg': data
    }

async def get_count(params):
    data = await lib.dao.test.get_test_list_count()
    return None, {
        'msg': data
    }


def get_test_list(params):
    # page = int(params['page'])
    # pagesize = int(params['pagesize'])
    data_list = lib.dao.test.get_fields_test_list(
        fields=[Test.test_id,Test.test_name]
    )
    # count = lib.dao.test.get_test_list_count()
    # result = com_func.pagination(
    #     data_list, count, page, pagesize
    # )
    return None, data_list
