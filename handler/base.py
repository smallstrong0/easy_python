# ! /usr/bin/env python
# -*- coding: utf-8 -*-

import tornado
import json
import traceback
from functools import wraps
from tornado.escape import json_decode
from tornado.web import RequestHandler, HTTPError, os
from lib.common import error
from lib.common.format import AlchemyJsonEncoder
from lib.common.aliyun_mysql import mysql_rds
from lib.common.error import CommonErrorType, CommonError
from lib.common.func import session_context_manage, get_time, get_ms, get_ts, deserialize, get_params_verify_sig, \
    get_mq_redis_context_manage, set_mq_redis_context_manage, get_params_without_sig
from lib.common.redis_queue import RedisQueue
from lib.common.const import REDIS_QUEUE_NAME
from handler import ylc_thread_pool

from tornado.ioloop import IOLoop

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
        self._mq_redis()

    def _create_session(self):
        session = mysql_rds.create_session()
        # print('session id is {}'.format(id(session)))
        session_context_manage.set(session)

    def _mq_redis(self):
        set_mq_redis_context_manage(obj=None, empty=True)

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
            if issubclass(error_cls, CommonError):
                err_r = kwargs['exc_info'][1]
                self.write_json(error=err_r.common_error)
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
            mq_redis = get_mq_redis_context_manage()
            if mq_redis:
                self.deal_mq_redis(mq_redis)
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

    def deal_mq_redis(self, mq_redis):
        for r_index in mq_redis:
            queue_name = r_index.get("queue")
            data = r_index.get("content")
            queue.put_queue(queue_name, data)

    def push_api_log(self, chunk):
        ts = get_ts()
        time_consuming = get_ms() - self.ts_ms_in
        date_time_in = self.date_time_in
        date_time_out = get_time()
        method = self.request.method
        url = '{}{}'.format(self.request.host, self.request.uri)
        url_index_list = self.request.uri.split('?')
        url_index = ''
        if len(url_index_list) > 0:
            url_index = url_index_list[0]
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
            'url_index': url_index,
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

    def async_task(self, keys={}, task_func=None, sig=True):
        return IOLoop.current().run_in_executor(ylc_thread_pool, self.do_task, keys, task_func, sig)

    async def do_task(self, keys, task_func, sig):
        try:
            mysql_rds.get_session()
            data = {}
            if sig:
                error, params = get_params_verify_sig(self.request, keys)
            else:
                error, params = get_params_without_sig(self.request, keys)
            if error is None:
                params['remote_ip'] = self.request.remote_ip
                error, data = await task_func(params)
        except Exception as e:
            traceback.print_exc()
            mysql_rds.rollback()
            error = e.common_error if hasattr(e, 'common_error') else (-1, '未知异常，请联系客服')
            data = {}
        finally:
            # print('session id is {}'.format(id(mysql_rds.get_session())))
            mysql_rds.close()

        return error, data


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
