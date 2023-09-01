# coding:utf-8

import handler.api.test as test

urls = [
    [r'/test/info', test.TestHandler],
    [r'/test/info/list', test.TestListHandler],
]
