#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 3/5/24 20:28
# @Author  : SmallStrong
# @Des     : 
# @File    : redis_test.py
# @Software: PyCharm
import asyncio
from lib.common.redis_util import redis_client

async def go():
    key ='haha'
    await redis_client.set_str_cache(
        key=key,
        str='11'
    )
    res = await redis_client.get_str_cache(
        key=key
    )
    print(res)

    await redis_client.delete_cache(
        key=key
    )

    await redis_client.set_hash_cache(
        name='ww',
        redis_dict={
            'a':1,
            'b':2
        }
    )

    await redis_client.hset_hash_cache(
        name='ww',
        key='c',
        value=3
    )

    res = await redis_client.get_hash_key(
        name='ww',
        key='c'
    )
    print(res)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(go())
    except RuntimeError as e:
        print(e)
    finally:
        loop.close()
