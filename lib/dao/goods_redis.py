#! /usr/bin/env python
# -*- coding: utf-8 -*-

# @Author: ss
# @Time: 2023-09-01 21:51:32
# @File: goods_redis.py

from lib.common.redis_key import GoodsRedis
from lib.common.redis_util import redis_client
from lib.common.func import serialize, deserialize


def set_goods_cache(key, data):
    redis_client.set_str_cache(key=GoodsRedis.UNIQUE_KEY.format(key), str=serialize(data), ex=GoodsRedis.EX)


def get_goods_cache(key):
    data = redis_client.get_str_cache(key=GoodsRedis.UNIQUE_KEY.format(key))
    if data:
        data = deserialize(data)
    else:
        data = {}
    return data


def delete_goods_cache(key):
    redis_client.delete_cache(key=GoodsRedis.UNIQUE_KEY.format(key))
