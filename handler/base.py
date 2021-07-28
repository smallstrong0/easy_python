# ! /usr/bin/env python
# -*- coding: utf-8 -*-

import json
import traceback
from functools import wraps
from tornado.escape import json_decode
from tornado.web import RequestHandler, HTTPError, os
from lib.common import error
from lib.common.format import AlchemyJsonEncoder
from lib.common.aliyun_mysql import mysql_rds
from lib.common.error import CommonErrorType, BMCError
from lib.common.utils import session_context_manage, get_time, get_ms,get_ts,deserialize
from lib.common.redis_queue import RedisQueue
from lib.common.const import REDIS_QUEUE_NAME
queue = RedisQueue(queue_name=REDIS_QUEUE_NAME['sys_api_log'])


class BaseHandler(RequestHandler):

    def __init__(self, application, request, **kwargs):
        RequestHandler.__init__(self, application, request, **kwargs)
        self.date_time_in = get_time()
        self.ts_ms_in = get_ms()
        self.set_header('Content-Type', 'application/json')
        if 'etag' in self.request.headers:
            self.request.headers.pop('etag')
        if self.settings['allow_remote_access']:
            self.access_control_allow()
        self._create_session()

    def _create_session(self):
        session = mysql_rds.create_session()
        session_context_manage.set(session)

    def get_path(self):
        return self.request.path

    def data_received(self, chunk):
        pass

    def access_control_allow(self):
        # 允许 JS 跨域调用
        self.set_header("Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS")
        self.set_header("Access-Control-Allow-Headers", "Content-Type, Depth, User-Agent, X-File-Size, "
                                                        "X-Requested-With, X-Requested-By, If-Modified-Since, "
                                                        "X-File-Name, Cache-Control, Token")
        self.set_header('Access-Control-Allow-Origin', '*')

    def get(self, *args, **kwargs):
        raise HTTPError(**error.status_0)

    def post(self, *args, **kwargs):
        raise HTTPError(**error.status_0)

    def put(self, *args, **kwargs):
        raise HTTPError(**error.status_0)

    def delete(self, *args, **kwargs):
        raise HTTPError(**error.status_0)

    def options(self, *args, **kwargs):
        if self.settings['allow_remote_access']:
            self.write("")

    def prepare(self):
        if self.request.body:
            # 没有Content-Type头部则默认为 json 格式
            if not self.request.headers.get('Content-Type') or self.request.headers.get(
                    'Content-Type') == 'application/json' or self.request.headers.get(
                'Content-Type') == 'application/json; charset=UTF-8':
                self.args = json_decode(self.request.body)

    def write_error(self, status_code, *args, **kwargs):
        if "exc_info" in kwargs:
            error_cls = kwargs['exc_info'][0]
            if issubclass(error_cls, BMCError):
                err_r = kwargs['exc_info'][1]
                self.write_json(error=err_r.bmc_error)
            else:
                lines = []
                for line in traceback.format_exception(*kwargs["exc_info"]):
                    lines.append(line)
                self.write_json(error=(200, '{}:{}'.format(str(kwargs['exc_info'][0]), str(kwargs['exc_info'][1]))))
        else:  # 不存在这种可能
            self.write_json(error=CommonErrorType.UNEXCEPT_ERROR.value)

    def write_json(self, error, data={}):
        if error is None:
            code = mysql_rds.finish()
            if code == -1:
                error = CommonErrorType.DATA_ERROR.value
        else:
            mysql_rds.rollback()
            mysql_rds.close()

        if error is None:
            chunk = {
                'code': 0,
                'data': data
            }
        else:
            chunk = {
                'code': error[0],
                'error_msg': error[1],
            }
        try:
            self.push_api_log(chunk)
        except Exception as e:
            pass
        self.finish(json.dumps(chunk, cls=AlchemyJsonEncoder, ensure_ascii=False))

    def push_api_log(self, chunk):
        ts = get_ts()
        time_consuming = get_ms() - self.ts_ms_in
        date_time_in = self.date_time_in
        date_time_out = get_time()
        method = self.request.method
        url = '{}{}'.format(self.request.host, self.request.uri)
        try:
            user_id = self.get_argument('user_id')
        except Exception as e:
            user_id = 0
        if not user_id:
            user_id = 0
        params = {}
        if self.request.arguments:
            params.update({elem[0]: elem[1][0].decode() for elem in self.request.arguments.items()})
        body = deserialize(self.request.body) or {}
        response = chunk

        msg_dict = {
            'ctime': ts,
            'mtime': ts,
            'time_consuming': time_consuming,
            'params': params,
            'body': body,
            'response': response,
            'date_time_in': date_time_in,
            'date_time_out': date_time_out,
            'method': method,
            'url': url,
            'user_id': user_id,
        }
        queue.put(msg_dict)


class APINotFoundHandler(BaseHandler):
    def data_received(self, chunk):
        pass

    def get(self, *args, **kwargs):
        raise HTTPError(**error.status_1)

    def post(self, *args, **kwargs):
        raise HTTPError(**error.status_1)

    def put(self, *args, **kwargs):
        raise HTTPError(**error.status_1)

    def delete(self, *args, **kwargs):
        raise HTTPError(**error.status_1)

    def options(self, *args, **kwargs):
        if self.settings['allow_remote_access']:
            self.write("")


def check_signature(func):
    @wraps(func)
    def check(self: BaseHandler, *args, **kwargs):
        # todo check func
        response = func(self, *args, **kwargs)
        return response

    return check
