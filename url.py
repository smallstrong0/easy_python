# coding:utf-8

from handler.base import APINotFoundHandler
from tornado.options import options
import handler.api.ss as ss
urls = [
    [r'/ss/test', ss.TestHandler],
    [r'.*', APINotFoundHandler],
]
for u in urls:
    u[0] = options.subpath + u[0]
