#! /usr/bin/env python
# -*- coding: utf-8 -*-

# @Author: ss
# @Time: 2023-09-01 21:51:32
# @File: goods.py

import lib.dao.goods_mysql as goods_mysql
import lib.dao.goods_redis as goods_redis
import lib.common.const as com_const
import lib.common.error as error_const
import lib.common.func as com_func
from sqlalchemy import  or_, and_, any_, text, exists, func, distinct, between, case

from lib.model.model import Goods

# 注意所有的sql都传列表类型
### add func #####

async def add_goods(obj):
    await goods_mysql.add_goods(
        data_obj=obj
    )

async def bulk_add_goods(data_list):
    await goods_mysql.bulk_add_goods(data_list=data_list)

### add func #####

### delete func #####
async def delete_goods(goods_id=-1):
    filters = []
    if goods_id != -1:
        filters.append(Goods.goods_id == goods_id)
    # goods_mysql.delete_goods(
    #     filters=filters
    # )
    await goods_mysql.update_goods(
        filters=filters,
        data_dict={
            'is_delete': 1,
            'mtime': com_func.get_ts()
        }
    )

### delete func #####

### update func #####
async def update_goods(goods_id=-1, data_dict={}):
    filters = []
    if goods_id != -1:
        filters.append(Goods.goods_id == goods_id)
    await goods_mysql.update_goods(
        filters=filters,
        data_dict=data_dict
    )

async def bulk_update_goods(data_list):
    await goods_mysql.bulk_update_goods(data_list=data_list)

### update func #####

### get one data func #####
async def get_goods(goods_id=-1):
    filters = [Goods.is_delete == 0]
    if goods_id != -1:
        filters.append(Goods.goods_id == goods_id)
    data = await goods_mysql.get_goods(
        query_list=[Goods],
        filters=filters,
    )
    return data

### get one data func #####

### get data_list func #####
async def get_goods_list_all(goods_id_list=-1):
    filters = [Goods.is_delete == 0]
    if goods_id_list != -1:
        filters.append(Goods.goods_id.in_(goods_id_list))
    order_by = [Goods.ctime.desc()]
    data_list = await goods_mysql.get_goods_list(
        query_list=[Goods],
        filters=filters,
        order_by=order_by,
    )
    return data_list


async def get_fields_goods_list_all(fields=[],goods_id_list=-1):
    if not fields:  # 注意重名多表字段取出的重名问题
        return []
    filters = [Goods.is_delete == 0]
    if goods_id_list != -1:
        filters.append(Goods.goods_id.in_(goods_id_list))
    order_by = [Goods.ctime.desc()]
    data_list = await goods_mysql.get_goods_list(
        query_list=[Goods],
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


async def get_fields_goods_list(fields=[], goods_id_list=-1, page=1, pagesize=10):
    if not fields:  # 注意重名多表字段取出的重名问题
        return []
    filters = [Goods.is_delete == 0]
    if goods_id_list != -1:
        filters.append(Goods.goods_id.in_(goods_id_list))
    order_by = [Goods.ctime.desc()]
    data_list = await goods_mysql.get_goods_list(
        query_list=[Goods],
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



async def get_goods_list(goods_id_list=-1, page=1, pagesize=10):
    filters = [Goods.is_delete == 0]
    if goods_id_list != -1:
        filters.append(Goods.goods_id.in_(goods_id_list))
    order_by = [Goods.ctime.desc()]
    data_list = await goods_mysql.get_goods_list(
        query_list=[Goods],
        filters=filters,
        order_by=order_by,
        offset=pagesize * int(page - 1),
        limit=pagesize
    )
    return data_list


async def get_goods_list_count(goods_id_list=-1):
    filters = [Goods.is_delete == 0]
    if goods_id_list != -1:
        filters.append(Goods.goods_id.in_(goods_id_list))
    count = await goods_mysql.get_goods_list_count(
        query_list=[func.count(Goods.goods_id)],
        filters=filters,
    )
    return count


### get data_list func #####
