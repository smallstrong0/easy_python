#! /usr/bin/env python
# -*- coding: utf-8 -*-

# @Author: ss
# @Time: 2020/7/22 9:53 上午
# @File: redis_key.py
import random

PROJECT = 'ss'
TYPE = 'cache'  # 设计type这个参数是为了上线版本之后的数据一致性，(当表结构存在修改的情况下)上线之前清理掉 ss:cache:开头的缓存
LOGIC_TYPE = 'hard'  # 设计type这个参数是为了上线版本之后的数据一致性，(当表结构存在修改的情况下)上线之前清理掉 ss:cache:开头的缓存
PREFIX = '{}:{}:'.format(PROJECT, TYPE)  # cache 前缀
LOGIC_PREFIX = '{}:{}:'.format(PROJECT, LOGIC_TYPE)  # 作为硬逻辑判断的cache 前缀 不可删除的类型（典型场景就是 计数）


# key 组成
# project:type:table:unique_key (unique_key大部分清空下就是主键)

class SequenceRedis(object):
    SEQUENCE_ID = "sequence_id:" + '{}'


# 测试相关
class TestRedis(object):
    UNIQUE_KEY = PREFIX + "test:" + '{}'
    EX = 86400 * 15 + random.randint(1800, 3600)


# 商品相关
class GoodsRedis(object):
    UNIQUE_KEY = PREFIX + "goods:"+'{}'
    EX = 86400 * 15 + random.randint(1800, 3600)
