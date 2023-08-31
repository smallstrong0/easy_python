#! /usr/bin/env python
# -*- coding: utf-8 -*-

# @Author: ss
# @Time: 2023-08-03 10:46:33
# @File: test_mysql.py

from lib.common.error import TestErrorType, CommonError
from lib.common.aliyun_mysql import mysql_rds
from lib.model.model import Test


async def add_test(data_obj):
    code = await mysql_rds.add(data_obj=data_obj)
    if code == -1:
        raise CommonError(TestErrorType.TEST_ADD_ERROR.value)


async def bulk_add_test(data_list):
    code = await mysql_rds.bulk_insert(data_list=data_list)
    if code == -1:
        raise CommonError(TestErrorType.TEST_BULK_ADD_ERROR.value)


async def delete_test(filters):
    code = await mysql_rds.delete(table=Test, filters=filters)
    if code == -1:
        raise CommonError(TestErrorType.TEST_DELETE_ERROR.value)


async def update_test(filters, data_dict):
    code = await mysql_rds.update(table=Test, filters=filters, data_dict=data_dict)
    if code == -1:
        raise CommonError(TestErrorType.TEST_UPDATE_ERROR.value)


async def bulk_update_test(data_list):
    code = await mysql_rds.bulk_update(table=Test, data_list=data_list)
    if code == -1:
        raise CommonError(TestErrorType.TEST_BULK_UPDATE_ERROR.value)


async def get_test(query_list=[], join=[], join_two=[], join_three=[], filters=[], group_by=[], order_by=[]):
    return await mysql_rds.find_one(query_list=query_list, join=join, join_two=join_two, join_three=join_three,
                                    filters=filters, group_by=group_by, order_by=order_by)


async def get_test_list(query_list=[], join=[], join_two=[], join_three=[], outerjoin=[], filters=[], group_by=[],
                        having=[], order_by=[], limit=0, offset=0):
    return await mysql_rds.find_list(query_list=query_list, join=join, join_two=join_two, join_three=join_three,
                                     outerjoin=outerjoin, filters=filters, group_by=group_by, having=having,
                                     order_by=order_by,
                                     limit=limit,
                                     offset=offset)


async def get_test_list_count(query_list=[], join=[], join_two=[], join_three=[], outerjoin=[], filters=[], group_by=[],
                              having=[],
                              order_by=[]):
    return await mysql_rds.count(query_list=query_list, join=join, join_two=join_two, join_three=join_three,
                                 outerjoin=outerjoin, filters=filters, group_by=group_by, having=having,
                                 order_by=order_by)


async def sql_execute(sql_str):
    return await mysql_rds.sql_execute(sql_str=sql_str)
