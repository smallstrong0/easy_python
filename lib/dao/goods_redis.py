#! /usr/bin/env python
# -*- coding: utf-8 -*-

# @Author: ss
# @Time: 2024-03-05 19:16:44
# @File: goods_redis.py

from lib.common.redis_key import GoodsRedis
from lib.common.redis_util import redis_client
from lib.common.func import serialize, deserialize


async def set_goods_cache(key, data):
    await redis_client.set_str_cache(key=GoodsRedis.UNIQUE_KEY.format(key), str=serialize(data), ex=GoodsRedis.EX)


async def get_goods_cache(key):
    data = await redis_client.get_str_cache(key=GoodsRedis.UNIQUE_KEY.format(key))
    if data:
        data = deserialize(data)
    else:
        data = {}
    return data


async def delete_goods_cache(key):
    await redis_client.delete_cache(key=GoodsRedis.UNIQUE_KEY.format(key))
