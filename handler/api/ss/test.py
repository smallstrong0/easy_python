#! /usr/bin/env python
# -*- coding: utf-8 -*-

# @Author: ss
# @Time: 2020-09-16 16:53:17
# @File: test.py


import lib.dap.test
import lib.common.utils

from handler.base import BaseHandler, check_signature
from tornado import gen


class TestListHandler(BaseHandler):
    # @check_signature
    @gen.coroutine
    def get(self):
        """
        @api {GET} /ss/demo/list todo: func list desc
        @apiGroup ss
        @apiVersion  1.3.1

        @apiDescription  系统:斑集后台、app、小程序<br>
                         模块：todo sub_desc <br>
                         功能：todo sub_desc

        @apiParam {Int} todo  params todo
        @apiParam {Int} page  页码
        @apiParam {Int} pagesize  每页多少条

        @apiSuccessExample {json} Request Example
        {
            "todo": 'req params todo',
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
                        "todo": 'resp params todo',
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
        error, params = lib.common.utils.get_params_verify_sig(self.request, keys)
        if error is None:
            error, data = lib.dap.test.get_test_list(params)
            self.write_json(error, data)
        else:
            self.write_json(error)


class TestHandler(BaseHandler):
    # @check_signature
    @gen.coroutine
    def get(self):
        """
        @api {GET} /ss/demo  todo: get func desc
        @apiGroup ss
        @apiVersion  1.3.1

        @apiDescription  系统:斑集后台、app、小程序<br>
                         模块：todo sub_desc <br>
                         功能：todo sub_desc

        @apiParam {Int} user_id  用户ID
        @apiParam {Int} todo  params todo


        @apiSuccessExample {json} Request Example
        {
            "user_id": 1789900001,
            "todo": 'req params todo',
        }
        @apiSuccessExample  {json} Response-Example
        {
            "code": 0,
            "data": {
                "todo": 'resp params todo',
            }
        }
        """
        keys = {
            'user_id': None,
            'ts': None,
            'nonce': None,
        }
        error, params = lib.common.utils.get_params_verify_sig(self.request, keys)
        if error is None:
            error, data = lib.dap.test.get_test(params)
            self.write_json(error, data)
        else:
            self.write_json(error)

    # @check_signature
    @gen.coroutine
    def post(self):
        """
        @api {POST} /ss/demo  todo: add func desc
        @apiGroup ss
        @apiVersion  1.3.1

        @apiDescription  系统:斑集后台、app、小程序<br>
                         模块：todo sub_desc <br>
                         功能：todo sub_desc

        @apiParam {Int} user_id  用户ID
        @apiParam {Int} todo  params todo


        @apiSuccessExample {json} Request Example
        {
            "user_id": 1789900001,
            "todo": 'req params todo',
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
        error, params = lib.common.utils.get_params_verify_sig(self.request, keys)
        if error is None:
            error, data = lib.dap.test.add_test(params)
            self.write_json(error, data)
        else:
            self.write_json(error)

    # @check_signature
    @gen.coroutine
    def put(self):
        """
        @api {PUT} /ss/demo  todo: update func desc
        @apiGroup ss
        @apiVersion  1.3.1

        @apiDescription  系统:斑集后台、app、小程序<br>
                         模块：todo sub_desc <br>
                         功能：todo sub_desc

        @apiParam {Int} user_id  用户ID
        @apiParam {Int} todo  params todo

        @apiSuccessExample {json} Request Example
        {
            "user_id": 1789900001,
            "todo": 'req params todo'
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
        error, params = lib.common.utils.get_params_verify_sig(self.request, keys)
        if error is None:
            error, data = lib.dap.test.update_test(params)
            self.write_json(error, data)
        else:
            self.write_json(error)

    # @check_signature
    @gen.coroutine
    def delete(self):
        """
        @api {DELETE} /ss/demo  todo: delete func desc
        @apiGroup ss
        @apiVersion  1.3.1

        @apiDescription  系统:斑集后台、app、小程序<br>
                         模块：todo sub_desc <br>
                         功能：todo sub_desc

        @apiParam {Int} user_id  用户ID
        @apiParam {Int} todo  params todo

        @apiSuccessExample {json} Request Example
        {
            "user_id": 1789900001,
            "todo": 'req params todo'
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
        error, params = lib.common.utils.get_params_verify_sig(self.request, keys)
        if error is None:
            error, data = lib.dap.test.delete_test(params)
            self.write_json(error, data)
        else:
            self.write_json(error)
