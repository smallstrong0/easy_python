#! /usr/bin/env python
# -*- coding: utf-8 -*-

# @Author: ss
# @Time: 2023-08-03 10:46:33
# @File: test_redis.py

from lib.common.redis_key import TestRedis
from lib.common.redis_util import redis_client
from lib.common.func import serialize, deserialize


async def set_test_cache(key, data):
    await redis_client.set_str_cache(key=TestRedis.UNIQUE_KEY.format(key), str=serialize(data), ex=TestRedis.EX)


async def get_test_cache(key):
    data = await redis_client.get_str_cache(key=TestRedis.UNIQUE_KEY.format(key))
    if data:
        data = deserialize(data)
    else:
        data = {}
    return data


async def delete_test_cache(key):
    await redis_client.delete_cache(key=TestRedis.UNIQUE_KEY.format(key))
