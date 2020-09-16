#! /usr/bin/env python
# -*- coding: utf-8 -*-

# @Author: ss
# @Time: 2020-09-16 16:53:17
# @File: test.py

import lib.dao.test_mysql as test_mysql
import lib.dao.test_redis as test_redis
import lib.common.const as com_const
import lib.common.error as error_const
import lib.common.utils as com_utils
from sqlalchemy import create_engine, or_, and_, any_, text, exists, func, distinct, between

from lib.model.model import Test

# 注意所有的sql都传列表类型
### add func #####

def add_test():
    # todo
    return

def bulk_add_test(data_list):
    return test_mysql.bulk_add_test(data_list=data_list)

### add func #####

### delete func #####
def delete_test():
    # todo
    return

### delete func #####

### update func #####
def update_test():
    # todo
    return

def bulk_update_test(data_list):
    return test_mysql.bulk_update_test(data_list=data_list)

### update func #####

### get one data func #####
def get_test():
    # todo
    return

### get one data func #####

### get data_list func #####
def get_test_list():
    # todo
    return

### get data_list func #####
