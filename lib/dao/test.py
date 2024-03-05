#! /usr/bin/env python
# -*- coding: utf-8 -*-

# @Author: ss
# @Time: 2023-08-03 10:46:33
# @File: test.py

import lib.dao.test_mysql as test_mysql
import lib.dao.test_redis as test_redis
import lib.common.const as com_const
import lib.common.error as error_const
import lib.common.func as com_func
from sqlalchemy import or_, and_, any_, text, exists, func, distinct, between, case

from lib.model.model import Test


# 注意所有的sql都传列表类型
### add func #####

async def add_test(obj):
    await test_mysql.add_test(
        data_obj=obj
    )


async def bulk_add_test(data_list):
    await test_mysql.bulk_add_test(data_list=data_list)


### add func #####

### delete func #####
async def delete_test(test_id=-1):
    filters = []
    if test_id != -1:
        filters.append(Test.test_id == test_id)
    await test_mysql.delete_test(
        filters=filters
    )
    # test_mysql.update_test(
    #     filters=filters,
    #     data_dict={
    #         'is_delete': 1,
    #         'mtime': com_func.get_ts()
    #     }
    # )


### delete func #####

### update func #####
async def update_test(test_id=-1, data_dict={}):
    filters = []
    if test_id != -1:
        filters.append(Test.test_id == test_id)
    await test_mysql.update_test(
        filters=filters,
        data_dict=data_dict
    )


async def bulk_update_test(data_list):
    await test_mysql.bulk_update_test(data_list=data_list)


### update func #####

### get one data func #####
async def get_test(fields=[], test_id=-1):
    filters = [Test.is_delete == 0]
    if test_id != -1:
        filters.append(Test.test_id == test_id)
    data = await test_mysql.get_test(
        query_list=fields if fields else [Test],
        filters=filters,
        group_by=[Test.test_id],
        order_by=[Test.ctime.desc()]
    )
    return data


### get one data func #####

### get data_list func #####
async def get_test_list(fields=[], fields_ret_dict=False, test_id_list=-1, page=0, pagesize=0):
    '''
    fields : 当要查询字段时候传入 fields
    fields_ret_dict ： 当 （仅仅要！！） 查询字段时候传入 True 时候，返回字典形式，key以数据库字段命名
    '''
    filters = [Test.is_delete == 0]
    if test_id_list != -1:
        filters.append(Test.test_id.in_(test_id_list))
    order_by = [Test.ctime.desc()]
    data_list = await test_mysql.get_test_list(
        query_list=fields if fields else [Test],
        filters=filters,
        order_by=order_by,
        offset=pagesize * int(page - 1) if pagesize else 0,
        limit=pagesize
    )
    if fields and fields_ret_dict:
        name_list = []
        for info in fields:
            key = info.key
            if key not in name_list:
                name_list.append(key)  # test_id
            else:
                name_list.append(info.expression)  # test.test_id
        name_list = [info.key for info in fields]
        data_list = [dict(zip(name_list, data)) for data in data_list]
    return data_list


async def get_test_list_count(test_id_list=-1):
    filters = [Test.is_delete == 1]
    if test_id_list != -1:
        filters.append(Test.test_id.in_(test_id_list))
    count = await test_mysql.get_test_list_count(
        query_list=[func.count(Test.test_id)],
        filters=filters,
    )
    return count

### get data_list func #####
