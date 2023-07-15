# coding:utf-8

import handler.api.test as test
from handler.base import APINotFoundHandler

urls = [

    [r'/test/info', test.TestHandler],
    [r'/test/info/list', test.TestListHandler],
    [r'.*', APINotFoundHandler],
]
