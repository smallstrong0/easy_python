#! /usr/bin/env python
# -*- coding: utf-8 -*-

# @Author: ss
# @Time: 2020/7/20 1:42 下午
# @File: run_test.py

import lib.common.func as com_func

ts = com_func.get_ts()

PUBLIC_PARAMS = {
    'bmc': {
            'ts': ts,
            'nonce': 472915,
            'sys_source': "PC",
            'sys_version': "V2.2.1",
            'sig': "a903bb9075b38158b3b2c1b8adda4aeebfd4e465",
            'user_id': 110294,
            "saas_role": "bmc",
            "belong_to": "1789900001",
            "debug": True,
            "page": 1,
            "pagesize": 10
        },
    'coc': {
            'ts': ts,
            'nonce': 472915,
            'sys_source': "PC",
            'sys_version': "V2.2.1",
            'sig': "a903bb9075b38158b3b2c1b8adda4aeebfd4e465",
            "saas_role": "coc",
            "belong_to": "1790000126",
            'user_id': 110083,
        },
    'store': {
            'ts': ts,
            'nonce': 472915,
            'sys_source': "PC",
            'sys_version': "V2.2.1",
            'sig': "a903bb9075b38158b3b2c1b8adda4aeebfd4e465",
            "store_id": 7682,
            "belong_to": "1789900001",
            "saas_role": "supplier",
            'user_id': 1846711197,
        },
    'user': {
            'ts': ts,
            'nonce': 472915,
            'sys_source': "APP",
            'sys_version': "V2.2.1",
            'sig': "a903bb9075b38158b3b2c1b8adda4aeebfd4e465",
            "user_id": 1276
    }
}