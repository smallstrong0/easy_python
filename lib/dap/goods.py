#! /usr/bin/env python
# -*- coding: utf-8 -*-

# @Author: ss
# @Time: 2023-09-01 21:51:32
# @File: goods.py

import lib.dao.goods
import lib.common.const as com_const
import lib.common.error as error_const
import lib.common.func as com_func
from lib.model.model import Goods
from lib.common.error import GoodsErrorType,CommonError
import lib.dao.sequence

async def add_goods(params):
    ts = com_func.get_ts()
    user_id = params['user_id']
    obj = Goods(
        ctime=ts,
        mtime=ts,
        create_by=user_id,
        update_by=user_id
    )
    await lib.dao.goods.add_goods(obj=obj)
    return None, {}


async def bulk_add_goods(params):
    ts = com_func.get_ts()
    user_id = params['user_id']
    info_list = params['info_list']
    data_list = []
    for info in info_list:
        data_list.append(
            Goods(
                ctime=ts,
                mtime=ts,
                create_by=user_id,
                update_by=user_id
            )
        )
    await lib.dao.goods.bulk_add_goods(data_list=data_list)
    return None, {}


async def update_goods(params):
    ts = com_func.get_ts()
    user_id = params['user_id']
    goods_id = params['goods_id']
    data_dict = {
        'mtime': ts,
        'update_by': user_id
    }
    await lib.dao.goods.update_goods(
        goods_id=goods_id,
        data_dict=data_dict
    )
    return None, {}


async def delete_goods(params):
    goods_id = params['goods_id']
    await lib.dao.goods.delete_goods(goods_id=goods_id)
    return None, {}


async def get_goods(params):
    goods_id = params['goods_id']
    data = await lib.dao.goods.get_goods(goods_id=goods_id)
    return None, data


async def get_goods_list(params):
    page = int(params['page'])
    pagesize = int(params['pagesize'])
    data_list = await lib.dao.goods.get_goods_list(
        page=page,
        pagesize=pagesize
    )
    count = await lib.dao.goods.get_goods_list_count()
    result = com_func.pagination(
        data_list, count, page, pagesize
    )
    return None, result