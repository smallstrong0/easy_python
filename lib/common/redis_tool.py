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


redis_obj = cli()
