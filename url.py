# coding:utf-8

import handler.api.goods as goods
import handler.api.test as test

urls = [
    [r'/test/info', test.TestHandler],
    [r'/test/info/list', test.TestListHandler],
    [r'/goods/info', goods.GoodsHandler],
    [r'/goods/info/list', goods.GoodsListHandler],
]
