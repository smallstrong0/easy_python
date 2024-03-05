#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 3/5/24 12:39
# @Author  : SmallStrong
# @Des     : 
# @File    : redis_tool.py
# @Software: PyCharm
import aioredis
import asyncio


class cli:
    def __init__(self, url):
        try:
            self.session = aioredis.from_url(
                "redis://localhost", encoding="utf-8", decode_responses=True
            )
        except Exception as e:
            raise

    async def set_str_cache(self, key, str, ex=60):
        """
        将内存数据二进制通过序列号转为文本流，再存入redis
        如果use_cache为False，表示不开启缓存，直接返回
        :param key: 缓存key，必须是str，且包含业务线，功能模块信息如
        supply-chain:user:info:100
        :param data: python对象不能
        :param ex: 缓存必须设置，默认60秒
        :return:
        """
        await self.session.set(key, str, ex)

    async def set_str_cache_no_ex(self, key, data):
        await self.session.set(key, data)

    async def get_str_cache(self, key):
        """
        将文本流从redis中读取并反序列化，返回
        如果use_cache为False，表示不开启缓存，直接返回
        :param key: 缓存key，必须是str
        :return:
        """
        result = await self.session.get(key)
        if result:
            result = bytes.decode(result)
        return result
    async def delete_cache(self, key):
        await self.session.delete(key)

    # hash结构存储
    async def set_hash_cache(self, name, redis_dict):
        await self.session.hmset(name, redis_dict)

    async def hset_hash_cache(self, name, key, value):
        return await self.session.hset(name, key, value)

    # hash中key的vaule的自增
    async def hincrby_hash_values(self, name, key, amount):
        await self.session.hincrby(name, key, amount=amount)

    async def get_hash_key(self, name, key):
        result = await self.session.hget(name, key)
        if result:
            result = bytes.decode(result)
        return result

    async def expireat_hash_cache(self, name, expire_time):
        await self.session.expireat(name, expire_time)

    async def setnx_cache(self, key, str):
        result = await self.session.setnx(key, str)
        return result

    async def expire_cache(self, key, ex=60):
        result = await self.session.expire(key, ex)
        return result

    async def zadd_zset_cache(self, name, mapping):
        return await self.session.zadd(name, mapping)

    async def zrem_zset_cache(self, name, member):
        result = await self.session.zrem(name, member)
        return result

    async def zcart_zset_cache(self, name):
        result = await self.session.zcard(name)
        return result

    async def zscore_zset_cache(self, name, member):
        result = await self.session.zscore(name, member)
        return result

    async def incr(self, k):  # 集合元素的数量
        return await self.session.incr(k)

    async def get_all_keys(self, name):
        result = await self.session.keys(pattern=name + '*')
        if result:
            result = [bytes.decode(i) for i in result]
        return result

    async def incrby(self, k, amount):
        return await self.session.incrby(k, amount)

    async def decrby(self, k, amount):
        return await self.session.decrby(k, amount)

    async def incr_amount(self, k, amount):
        return await self.session.incr(k, amount)

redis_client = cli()
