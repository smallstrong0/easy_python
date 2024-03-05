#! /usr/bin/env python
# -*- coding: utf-8 -*-

# @Author: ss
# @Time: 2024-03-05 19:16:44
# @File: goods.py


import lib.dap.goods
import lib.common.func as com_func
from handler.base import BaseHandler


class GoodsListHandler(BaseHandler):
    async def post(self):
        """
        @api {POST} /goods/info/list   商品列表
        @apiGroup goods
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
        error, data = await self.do_task(keys=keys, task_func=lib.dap.goods.get_goods_list, sig=True)
        if error is None:
            self.write_json(error, data)
        else:
            self.write_json(error)


class GoodsHandler(BaseHandler):
    async def post(self):
        """
        @api {POST} /goods/info  商品添加
        @apiGroup goods
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
        error, data = await self.do_task(keys=keys, task_func=lib.dap.goods.add_goods, sig=True)
        if error is None:
            self.write_json(error, data)
        else:
            self.write_json(error)

    async def put(self):
        """
        @api {PUT} /goods/info  商品修改
        @apiGroup goods
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
        error, data = await self.do_task(keys=keys, task_func=lib.dap.goods.update_goods, sig=True)
        if error is None:
            self.write_json(error, data)
        else:
            self.write_json(error)

    async def delete(self):
        """
        @api {DELETE} /goods/info  商品删除
        @apiGroup goods
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
        error, data = await self.do_task(keys=keys, task_func=lib.dap.goods.delete_goods, sig=True)
        if error is None:
            self.write_json(error, data)
        else:
            self.write_json(error)

    async def get(self):
        """
        @api {GET} /goods/info  商品详情
        @apiGroup goods
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
            'user_id': None,
            'ts': None,
            'nonce': None,
        }
        error, data = await self.do_task(keys=keys, task_func=lib.dap.goods.get_goods, sig=True)
        if error is None:
            self.write_json(error, data)
        else:
            self.write_json(error)
