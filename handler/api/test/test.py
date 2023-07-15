#! /usr/bin/env python
# -*- coding: utf-8 -*-

# @Author: ss
# @Time: 2023-07-11 16:06:08
# @File: test.py


import lib.dap.test
import lib.common.func as com_func
from handler.base import BaseHandler
from tornado import gen
from tornado.ioloop import IOLoop
from handler import ylc_thread_pool
from asgiref.sync import sync_to_async
from lib.common.aliyun_mysql import mysql_rds


class TestListHandler(BaseHandler):
    def post(self):
        """
        @api {POST} /test/info/list   测试列表
        @apiGroup test
        @apiVersion  1.0.0


        @apiParam {Int} page  页码
        @apiParam {Int} pagesize  每页多少条

        @apiSuccessExample {json} Request Example
        {
            "user_id": 1789900001,
            "page": 1,
            "pagesize": 10,
        }

        @apiSuccessExample  {json} Response-Example
        {
            "code": 0,
            "data": {
                "data_list": [
                    {
                    }
                ],
                "total_page": 2,
                "page": 1,
                "total_count": 15,
                "has_next": true
            }
        }
        """
        keys = {
            'user_id': None,
            'ts': None,
            'nonce': None,
            "page": 1,
            "pagesize": 10,
        }
        params, error = com_func.get_params_verify_sig(self.request, keys)
        if error is None:
            error, data = lib.dap.test.get_test_list(params)
            self.write_json(error, data)
        else:
            self.write_json(error)


class TestHandler(BaseHandler):
    @gen.coroutine
    def post(self):
        """
        @api {POST} /test/info  测试添加
        @apiGroup test
        @apiVersion  1.0.0


        @apiParam {Int} user_id  用户ID


        @apiSuccessExample {json} Request Example
        {
            "user_id": 1789900001,
        }
        @apiSuccessExample  {json} Response-Example
        {
            "code": 0,
            "data": {}
        }
        """
        keys = {
            'user_id': None,
            'ts': None,
            'nonce': None,
        }
        params, error = com_func.get_params_verify_sig(self.request, keys)
        if error is None:
            error, data = lib.dap.test.add_test(params)
            self.write_json(error, data)
        else:
            self.write_json(error)

    @gen.coroutine
    def put(self):
        """
        @api {PUT} /test/info  测试修改
        @apiGroup test
        @apiVersion  1.0.0


        @apiParam {Int} user_id  用户ID

        @apiSuccessExample {json} Request Example
        {
            "user_id": 1789900001,
        }
        @apiSuccessExample  {json} Response-Example
        {
            "code":0,
            "data": {}
        }
        """
        keys = {
            'user_id': None,
            'ts': None,
            'nonce': None,
        }
        params, error = com_func.get_params_verify_sig(self.request, keys)
        if error is None:
            error, data = lib.dap.test.update_test(params)
            self.write_json(error, data)
        else:
            self.write_json(error)

    @gen.coroutine
    def delete(self):
        """
        @api {DELETE} /test/info  测试删除
        @apiGroup test
        @apiVersion  1.0.0


        @apiParam {Int} user_id  用户ID

        @apiSuccessExample {json} Request Example
        {
            "user_id": 1789900001,
        }
        @apiSuccessExample  {json} Response-Example
        {
            "code":0,
            "data": {}
        }
        """
        keys = {
            'user_id': None,
            'ts': None,
            'nonce': None,
        }
        params, error = com_func.get_params_verify_sig(self.request, keys)
        if error is None:
            error, data = lib.dap.test.delete_test(params)
            self.write_json(error, data)
        else:
            self.write_json(error)

    async def get(self):
        """
        @api {GET} /test/info  测试详情
        @apiGroup test
        @apiVersion  1.0.0


        @apiParam {Int} user_id  用户ID


        @apiSuccessExample {json} Request Example
        {
            "user_id": 1789900001,
        }
        @apiSuccessExample  {json} Response-Example
        {
            "code": 0,
            "data": {
            }
        }
        """
        keys = {
        }
        error, data = await self.do_task(keys, lib.dap.test.get_test, False)
        if error is None:
            print('end is {}'.format(com_func.get_ts()))
            session = mysql_rds.get_session()
            print(id(session))
            self.write_json(error, data)
        else:
            self.write_json(error)
