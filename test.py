#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 3/5/24 15:24
# @Author  : SmallStrong
# @Des     : 
# @File    : test.py
# @Software: PyCharm

import asyncio
import aiohttp


async def main():

    async with aiohttp.ClientSession() as session:
        async with session.get('http://127.0.0.1:2222/ss/test/info/list') as response:

            print("Status:", response.status)
            print("Content-type:", response.headers['content-type'])

            html = await response.text()
            print(html)

asyncio.run(main())