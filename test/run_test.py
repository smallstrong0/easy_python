#! /usr/bin/env python
# -*- coding: utf-8 -*-

# @Author: ss
# @Time: 2020/7/20 1:42 下午
# @File: run_test.py


import unittest

ENV = 'local'
ENV_URL = {
    'local': 'http://127.0.0.1:7003',
    'dev': 'https://banji-dev.banmacang.com',
    'test': 'https://banji-test.banmacang.com',
    'demo': 'https://banji-demo.banmacang.com',
    'prod': 'https://banji-prod.banmacang.com',
}

if __name__ == '__main__':
    testLoader = unittest.TestLoader()
    suites = testLoader.discover(start_dir='../test', pattern='test*.py', top_level_dir='../test')
    runner = unittest.TextTestRunner()
    runner.run(suites)
