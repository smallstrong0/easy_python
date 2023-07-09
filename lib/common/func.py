#! /usr/bin/env python
# -*- coding: utf-8 -*-

# @Author: ss
# @Time: 2020/7/23 2:07 下午
# @File: utils.py

import contextvars
import json
import lib.common.error as com_error
import time

session_context_manage = contextvars.ContextVar('session')
mq_redis_context_manage = contextvars.ContextVar('mq_redis')


def get_mq_redis_context_manage():
    try:
        tmp_manage = mq_redis_context_manage.get()
    except:
        tmp_manage = []
    return tmp_manage


def set_mq_redis_context_manage(obj, empty=False):
    if empty:
        mq_redis_context_manage.set([])
    else:
        last_manage = get_mq_redis_context_manage()
        last_manage.append(obj)
        mq_redis_context_manage.set(last_manage)


def get_time(ts=None):
    if ts is None:
        ts = get_ts()
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(ts))


def get_ts():
    return int(time.time())


def get_ms():
    return int(time.time() * 1000)


def deserialize(data):
    """json 字符串转换成字典"""
    try:
        return json.loads(data)
    except Exception as e:
        # print e
        return None


def serialize(data, ensure_ascii=False):
    try:
        return json.dumps(data, ensure_ascii=ensure_ascii, separators=(',', ':'))
    except Exception as e:
        print(e)
        return None


def sort_serialize(data, ensure_ascii=False):
    try:
        return json.dumps(data, ensure_ascii=ensure_ascii, sort_keys=True, indent=4)
    except Exception as e:
        print(e)
        return None


def get_params_without_sig(request, keys):
    error, params = get_web_params(request, keys)
    return error, params


def get_params_verify_sig(request, keys):
    error, params = get_web_params(request, keys)
    # do sig
    return error, params


def get_web_params(request, keys):
    arguments = request.arguments
    body = request.body
    params = {}
    if arguments:
        """转码"""
        params.update({elem[0]: elem[1][0].decode() for elem in arguments.items()})
    if body and deserialize(body):
        params.update(deserialize(body))
    for key in keys:
        value = keys[key]
        if key not in params:
            if isinstance(value, tuple):
                length = len(value)
                if length == 1:
                    if value[0] is None:
                        return (-1, 'param <{}> is missing'.format(key)), {}
                    else:
                        params[key] = value[0]
                elif length == 2:
                    if value[0] is None:
                        return (-1, 'param <{}> is missing'.format(key)), {}
                    else:
                        params[key] = value[0]
                elif length == 3:
                    if value[0] is None:
                        return (-1, 'param <{}> is missing'.format(key)), {}
                    else:
                        params[key] = value[0]
            else:
                if value is None:
                    return (-1, 'param <{}> is missing'.format(key)), {}
                else:
                    params[key] = value
        else:
            if isinstance(value, tuple):
                _type = ''
                value_range = []
                length = len(value)
                if length == 2:
                    _type = value[1]
                elif length == 3:
                    _type = value[1]
                    value_range = value[2]
                if _type:
                    if _type == int:
                        try:
                            params[key] = int(params[key])
                        except Exception as e:
                            raise com_error.CommonError((-1, 'param <{}> is int type'.format(key)))
                    elif _type == str:
                        try:
                            params[key] = str(params[key])
                        except Exception as e:
                            raise com_error.CommonError((-1, 'param <{}> is str type'.format(key)))
                    elif _type == list:
                        try:
                            params[key] = list(params[key])
                        except Exception as e:
                            raise com_error.CommonError((-1, 'param <{}> is list type'.format(key)))
                    elif _type == dict:
                        try:
                            params[key] = dict(params[key])
                        except Exception as e:
                            raise com_error.CommonError((-1, 'param <{}> is dict type'.format(key)))
                    elif _type == bool:
                        try:
                            params[key] = bool(params[key])
                        except Exception as e:
                            raise com_error.CommonError((-1, 'param <{}> is bool type'.format(key)))
                if value_range:
                    if params[key] not in value_range:
                        raise com_error.CommonError((-1, 'param <{}> is not in values of {}'.format(key, value_range)))

    return None, params


def pagination(data_list, total_count, page, pagesize):
    """
    列表分页统一字段
    """
    if page == -1 and pagesize == -1:
        result = {
            'data_list': data_list,
            'total_page': 1,
            'page': 1,
            'total_count': total_count,
            'has_next': False,
        }
        return result
    max_page = int(total_count / pagesize) if total_count % pagesize == 0 else int(total_count / pagesize) + 1
    has_next = True if total_count > page * pagesize else False
    result = {
        'data_list': data_list,
        'total_page': max_page,
        'page': page,
        'total_count': total_count,
        'has_next': has_next,
    }
    return result