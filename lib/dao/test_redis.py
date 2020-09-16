#! /usr/bin/env python
# -*- coding: utf-8 -*-

# @Author: ss
# @Time: 2020-09-16 16:53:17
# @File: test_redis.py

from lib.common.redis_key import TestRedis
from lib.common.redis_util import redis_client
from lib.common.utils import serialize, deserialize


def set_test_cache(key, data):
    redis_client.set_str_cache(key=TestRedis.UNIQUE_KEY.format(key), str=serialize(data), ex=TestRedis.EX)


def get_test_cache(key):
    data = redis_client.get_str_cache(key=TestRedis.UNIQUE_KEY.format(key))
    if data:
        data = deserialize(data)
    else:
        data = {}
    return data


def delete_test_cache(key):
    redis_client.delete_cache(key=TestRedis.UNIQUE_KEY.format(key))
