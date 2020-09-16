# coding:utf-8

from handler.base import APINotFoundHandler
from tornado.options import options

urls = [
    [r'.*', APINotFoundHandler],
]
for u in urls:
    u[0] = options.subpath + u[0]
