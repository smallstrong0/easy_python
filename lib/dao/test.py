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
from sqlalchemy import  or_, and_, any_, text, exists, func, distinct, between, case

from lib.model.model import Test

# 注意所有的sql都传列表类型
### add func #####

def add_test(obj):
    test_mysql.add_test(
        data_obj=obj
    )

def bulk_add_test(data_list):
    test_mysql.bulk_add_test(data_list=data_list)

### add func #####

### delete func #####
def delete_test(test_id=-1):
    filters = []
    if test_id != -1:
        filters.append(Test.test_id == test_id)
    # test_mysql.delete_test(
    #     filters=filters
    # )
    test_mysql.update_test(
        filters=filters,
        data_dict={
            'is_delete': 1,
            'mtime': com_func.get_ts()
        }
    )

### delete func #####

### update func #####
def update_test(test_id=-1, data_dict={}):
    filters = []
    if test_id != -1:
        filters.append(Test.test_id == test_id)
    test_mysql.update_test(
        filters=filters,
        data_dict=data_dict
    )

def bulk_update_test(data_list):
    test_mysql.bulk_update_test(data_list=data_list)

### update func #####

### get one data func #####
def get_test(test_id=-1):
    filters = [Test.is_delete == 0]
    if test_id != -1:
        filters.append(Test.test_id == test_id)
    data = test_mysql.get_test(
        query_list=[Test],
        filters=filters,
    )
    return data

### get one data func #####

### get data_list func #####
def get_test_list_all(test_id_list=-1):
    filters = [Test.is_delete == 0]
    if test_id_list != -1:
        filters.append(Test.test_id.in_(test_id_list))
    order_by = [Test.ctime.desc()]
    data_list = test_mysql.get_test_list(
        query_list=[Test],
        filters=filters,
        order_by=order_by,
    )
    return data_list


def get_fields_test_list_all(fields=[],test_id_list=-1):
    if not fields:  # 注意重名多表字段取出的重名问题
        return []
    filters = [Test.is_delete == 0]
    if test_id_list != -1:
        filters.append(Test.test_id.in_(test_id_list))
    order_by = [Test.ctime.desc()]
    data_list = test_mysql.get_test_list(
        query_list=[Test],
        filters=filters,
        order_by=order_by,
    )
    if len(fields) == 1:
        return data_list  # 一般是取列表
    else:
        name_list = []
        for info in fields:
            key = info.key
            if key not in name_list:
                name_list.append(key)  # test_id
            else:
                name_list.append(info.expression)  # test.test_id
        name_list = [info.key for info in fields]
        res = [dict(zip(name_list, data)) for data in data_list]
        return res


def get_fields_test_list(fields=[], test_id_list=-1, page=1, pagesize=10):
    if not fields:  # 注意重名多表字段取出的重名问题
        return []
    filters = [Test.is_delete == 0]
    if test_id_list != -1:
        filters.append(Test.test_id.in_(test_id_list))
    order_by = [Test.ctime.desc()]
    data_list = test_mysql.get_test_list(
        query_list=[Test],
        filters=filters,
        order_by=order_by,
        offset=pagesize * int(page - 1),
        limit=pagesize
    )
    if len(fields) == 1:
        return data_list  # 一般是取列表
    else:
        name_list = []
        for info in fields:
            key = info.key
            if key not in name_list:
                name_list.append(key)
            else:
                name_list.append(info.expression)
        name_list = [info.key for info in fields]
        res = [dict(zip(name_list, data)) for data in data_list]
        return res



def get_test_list(test_id_list=-1, page=1, pagesize=10):
    filters = [Test.is_delete == 0]
    if test_id_list != -1:
        filters.append(Test.test_id.in_(test_id_list))
    order_by = [Test.ctime.desc()]
    data_list = test_mysql.get_test_list(
        query_list=[Test],
        filters=filters,
        order_by=order_by,
        offset=pagesize * int(page - 1),
        limit=pagesize
    )
    return data_list


def get_test_list_count(test_id_list=-1):
    filters = [Test.is_delete == 0]
    if test_id_list != -1:
        filters.append(Test.test_id.in_(test_id_list))
    count = test_mysql.get_test_list_count(
        query_list=[func.count(Test.test_id)],
        filters=filters,
    )
    return count


### get data_list func #####
