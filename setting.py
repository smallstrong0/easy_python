# -*- coding: utf-8 -*-

# 基础配置
debug = True
env = 'test'
port = 2222
subpath = 'ss'

# TOKEN 有效期15天，过期登录更新TOKEN,否着不变
TOKEN_EXPIRATION = 15 * 24 * 3600
# MySQLConfig
MYSQL = 'mysql+aiomysql://root:wangxiaoqiang@localhost:3306/tdh?charset=utf8'
# Redis Config
REDIS = {
    'HOST': '127.0.0.1',
    'USE_REDIS_CACHE': True,
    'PASSWORD': '',
    'PORT': 6379,
    'DB': 0,
}
