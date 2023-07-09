#! /usr/bin/env python
# -*- coding: utf-8 -*-

# @Author: ss
# @Time: 2020-09-16 16:53:17
# @File: test_mysql.py

from lib.common.error import TestErrorType,CommonError
from lib.common.aliyun_mysql import mysql_rds
from lib.model.model import Test


def add_test(data_obj):
    code = mysql_rds.add(data_obj=data_obj)
    if code == -1:
        raise CommonError(TestErrorType.TEST_ADD_ERROR.value)


def bulk_add_test(data_list):
    code = mysql_rds.bulk_insert(table=Test, data_list=data_list)
    if code == -1:
        raise CommonError(TestErrorType.TEST_BULK_ADD_ERROR.value)


def delete_test(filters):
    code = mysql_rds.delete(table=Test, filters=filters)
    if code == -1:
        raise CommonError(TestErrorType.TEST_DELETE_ERROR.value)


def update_test(filters, data_dict):
    code = mysql_rds.update(table=Test, filters=filters, data_dict=data_dict)
    if code == -1:
        raise CommonError(TestErrorType.TEST_UPDATE_ERROR.value)


def bulk_update_test(data_list):
    code = mysql_rds.bulk_update(table=Test, data_list=data_list)
    if code == -1:
        raise CommonError(TestErrorType.TEST_BULK_UPDATE_ERROR.value)


def get_test(query_list=[], join=[], join_two=[], join_three=[], filters=[], group_by=[], order_by=[]):
    return mysql_rds.find_one(query_list=query_list, join=join, join_two=join_two, join_three=join_three, filters=filters, group_by=group_by ,order_by=order_by)


def get_test_list(query_list=[], join=[], join_two=[], join_three=[], outerjoin=[], filters=[], group_by=[], order_by=[], limit=0, offset=0):
    return mysql_rds.find_list(query_list=query_list, join=join, join_two=join_two, join_three=join_three,
                               outerjoin=outerjoin, filters=filters, group_by=group_by, order_by=order_by,
                               limit=limit,
                               offset=offset)


def get_test_list_count(query_list=[], join=[], join_two=[], join_three=[], outerjoin=[], filters=[], group_by=[],
                        order_by=[]):
    return mysql_rds.count(query_list=query_list, join=join, join_two=join_two, join_three=join_three,
                           outerjoin=outerjoin, filters=filters, group_by=group_by, order_by=order_by)


def sql_execute(sql_str):
    return mysql_rds.sql_execute(sql_str=sql_str)


# 子查询 慎用
def get_test_subquery(query_list=[], join=[], join_two=[], join_three=[], outerjoin=[], filters=[]):
    return mysql_rds.subquery(query_list=query_list, join=join, join_two=join_two, outerjoin=outerjoin,
                              join_three=join_three,
                              filters=filters)
