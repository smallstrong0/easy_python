#! /usr/bin/env python
# -*- coding: utf-8 -*-

# @Author: ss
# @Time: 2023-07-11 16:06:08
# @File: test.py

import unittest
import requests
from test.run_test import ENV, ENV_URL
from test.common import PUBLIC_PARAMS
import json

BASE_URL = ENV_URL[ENV]


class TestTest(unittest.TestCase):

    def setUp(self):
        pass

    def test_test1_add(self):
        url = '{}{}'.format(BASE_URL, '/banji-api/test/info')
        body = {
        }

        params_url = ''
        params = {
        }
        params.update(PUBLIC_PARAMS['bmc'])
        for key in params:
            params_url = params_url + '{}={}&'.format(key, params[key])
        if params_url.endswith('&'):
            params_url = params_url[0:len(params_url) - 1]
        url = url + '?' + params_url

        # body.update(PUBLIC_PARAMS['bmc']) # 公共参数抽取,自行修改接口调用的角色
        resp = requests.post(url=url, json=body)
        if resp.status_code == 200 and resp.text:
            data = json.loads(resp.text)
            self.assertEqual(data['code'], 0, "添加通过")
        else:
            self.assertEqual(1, 0, "添加失败")

    def test_test2_update(self):
        url = '{}{}'.format(BASE_URL, '/banji-api/test/info')
        body = {
        }

        params_url = ''
        params = {
        }
        params.update(PUBLIC_PARAMS['bmc'])
        for key in params:
            params_url = params_url + '{}={}&'.format(key, params[key])
        if params_url.endswith('&'):
            params_url = params_url[0:len(params_url) - 1]
        url = url + '?' + params_url

        # body.update(PUBLIC_PARAMS['bmc']) # 公共参数抽取,自行修改接口调用的角色
        resp = requests.put(url=url, json=body)
        if resp.status_code == 200 and resp.text:
            data = json.loads(resp.text)
            self.assertEqual(data['code'], 0, "修改通过")
        else:
            self.assertEqual(1, 0, "修改失败")

    def test_test3_get(self):
        url = '{}{}'.format(BASE_URL, '/banji-api/test/info')
        params = {
        }
        params.update(PUBLIC_PARAMS['bmc']) # 公共参数抽取,自行修改接口调用的角色
        params_url = ''
        for key in params:
            params_url = params_url + '{}={}&'.format(key, params[key])
        if params_url.endswith('&'):
            params_url = params_url[0:len(params_url) - 1]
        url = url + '?' + params_url
        resp = requests.get(url=url)
        if resp.status_code == 200 and resp.text:
            data = json.loads(resp.text)
            self.assertEqual(data['code'], 0, "详情通过")
        else:
            self.assertEqual(1, 0, "详情失败")

    def test_test4_get_list(self):
        url = '{}{}'.format(BASE_URL, '/banji-api/test/info/list')
        params = {
        }
        params.update(PUBLIC_PARAMS['bmc']) # 公共参数抽取,自行修改接口调用的角色
        params_url = ''
        for key in params:
            params_url = params_url + '{}={}&'.format(key, params[key])
        if params_url.endswith('&'):
            params_url = params_url[0:len(params_url) - 1]
        url = url + '?' + params_url
        resp = requests.get(url=url)
        if resp.status_code == 200 and resp.text:
            data = json.loads(resp.text)
            self.assertEqual(data['code'], 0, "列表通过")
        else:
            self.assertEqual(1, 0, "列表失败")

    def test_test5_delete(self):
        url = '{}{}'.format(BASE_URL, '/banji-api/test/info')
        body = {
        }

        params_url = ''
        params = {
        }
        params.update(PUBLIC_PARAMS['bmc'])
        for key in params:
            params_url = params_url + '{}={}&'.format(key, params[key])
        if params_url.endswith('&'):
            params_url = params_url[0:len(params_url) - 1]
        url = url + '?' + params_url

        # body.update(PUBLIC_PARAMS['bmc']) # 公共参数抽取,自行修改接口调用的角色
        resp = requests.delete(url=url, json=body)
        if resp.status_code == 200 and resp.text:
            data = json.loads(resp.text)
            self.assertEqual(data['code'], 0, "删除通过")
        else:
            self.assertEqual(1, 0, "删除失败")

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()
