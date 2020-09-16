# -*- coding: utf-8 -*-

#  设置调试模式：
debug = True

settings = {
    "cookie_secret": "61oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
    "login_url": "/login",
    "xsrf_cookies": True,
}
# TOKEN 有效期15天，过期登录更新TOKEN,否着不变
TOKEN_EXPIRATION = 15 * 24 * 3600
# MySQLConfig
MYSQL = 'mysql+pymysql://root:wangxiaoqiang@localhost:3306/test?charset=utf8'

# Redis Config
REDIS = {
    'HOST': '',
    'PASSWORD': '',
    'PORT': 6379,
    'DB': 0,
}
