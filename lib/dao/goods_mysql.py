#! /usr/bin/env python
# -*- coding: utf-8 -*-

# @Author: ss
# @Time: 2023-09-01 21:51:32
# @File: goods_mysql.py

from lib.common.error import GoodsErrorType,CommonError
from lib.common.aliyun_mysql import mysql_rds
from lib.model.model import Goods


async def add_goods(data_obj):
    code = await mysql_rds.add(data_obj=data_obj)
    if code == -1:
        raise CommonError(GoodsErrorType.GOODS_ADD_ERROR.value)


async def bulk_add_goods(data_list):
    code = await mysql_rds.bulk_insert(table=Goods, data_list=data_list)
    if code == -1:
        raise CommonError(GoodsErrorType.GOODS_BULK_ADD_ERROR.value)


async def delete_goods(filters):
    code = await mysql_rds.delete(table=Goods, filters=filters)
    if code == -1:
        raise CommonError(GoodsErrorType.GOODS_DELETE_ERROR.value)


async def update_goods(filters, data_dict):
    code = await mysql_rds.update(table=Goods, filters=filters, data_dict=data_dict)
    if code == -1:
        raise CommonError(GoodsErrorType.GOODS_UPDATE_ERROR.value)


async def bulk_update_goods(data_list):
    code = await mysql_rds.bulk_update(table=Goods, data_list=data_list)
    if code == -1:
        raise CommonError(GoodsErrorType.GOODS_BULK_UPDATE_ERROR.value)


async def get_goods(query_list=[], join=[], join_two=[], join_three=[], filters=[], group_by=[], order_by=[]):
    return await mysql_rds.find_one(query_list=query_list, join=join, join_two=join_two, join_three=join_three, filters=filters, group_by=group_by ,order_by=order_by)


async def get_goods_list(query_list=[], join=[], join_two=[], join_three=[], outerjoin=[], filters=[], group_by=[], having=[], order_by=[], limit=0, offset=0):
    return await mysql_rds.find_list(query_list=query_list, join=join, join_two=join_two, join_three=join_three,
                               outerjoin=outerjoin, filters=filters, group_by=group_by, having=having, order_by=order_by,
                               limit=limit,
                               offset=offset)


async def get_goods_list_count(query_list=[], join=[], join_two=[], join_three=[], outerjoin=[], filters=[], group_by=[], having=[],
                        order_by=[]):
    return await mysql_rds.count(query_list=query_list, join=join, join_two=join_two, join_three=join_three,
                           outerjoin=outerjoin, filters=filters, group_by=group_by, having=having, order_by=order_by)


async def sql_execute(sql_str):
    return await mysql_rds.sql_execute(sql_str=sql_str)



