#! /usr/bin/env python
# -*- coding: utf-8 -*-

# @Author: ss
# @Time: 2023-07-11 16:06:08
# @File: test.py

import lib.dao.test_mysql as test_mysql
import lib.dao.test_redis as test_redis
import lib.common.const as com_const
import lib.common.error as error_const
import lib.common.func as com_func
from sqlalchemy import create_engine, or_, and_, any_, text, exists, func, distinct, between

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
