#! /usr/bin/env python
# -*- coding: utf-8 -*-

# @Author: ss
# @Time: 2020/9/1 9:31 上午
# @File: sys_api_log.py
# !/usr/bin/env python
# -*- coding: utf-8 -*-


import lib.common.error as com_const_error
import lib.common.utils as func
import lib.common.aliyun_mysql
from lib.common.redis_queue import RedisQueue
from lib.common.const import REDIS_QUEUE_NAME
import traceback
from lib.model.model import ApiLog

DELETE_TS = func.get_ts() - 90 * 86400
mysql_rds = lib.common.aliyun_mysql.mysql_rds
queue = RedisQueue(queue_name=REDIS_QUEUE_NAME['sys_api_log'])
queue_error = RedisQueue(queue_name=REDIS_QUEUE_NAME['sys_api_log_error'])


def sys_log():
    mysql_rds.get_session()
    mysql_rds.delete(table=ApiLog, filters={
        ApiLog.ctime < DELETE_TS
    })
    mysql_rds.finish()
    while 1:
        for msg in queue.consume():
            try:
                error = deal_sys_log(msg)
                if error is not None:
                    print(error)
                    msg['error_msg'] = error
                    queue_error.put(msg)
            except Exception as e:
                queue_error.put(msg)
                traceback.print_exc()
                print(e)


def deal_sys_log(msg_dict):
    error = None
    session = mysql_rds.get_session()
    ctime = msg_dict['ctime']
    mtime = msg_dict['mtime']
    time_consuming = msg_dict['time_consuming']
    params = func.serialize(msg_dict['params'])
    body = func.serialize(msg_dict['body'])
    code = msg_dict['response'].get('code', '')
    if code == 0:
        result = 'SUCCESS'
    else:
        result = 'FAILED'
    response = func.serialize(msg_dict['response'])
    date_time_in = msg_dict['date_time_in']
    date_time_out = msg_dict['date_time_out']
    method = msg_dict['method']
    url = msg_dict['url']
    user_id = msg_dict['user_id']
    api_log = ApiLog(
        ctime=int(ctime),
        mtime=int(mtime),
        time_consuming=int(time_consuming),
        params=params,
        body=body,
        response=response,
        date_time_in=date_time_in,
        date_time_out=date_time_out,
        method=method,
        url=url,
        user_id=user_id,
        result=result
    )
    code = mysql_rds.add(data_obj=api_log)
    if code != 0:
        error = com_const_error.CommonErrorType.UNEXCEPT_ERROR.value
    if error is None:
        code = mysql_rds.session_maker(session)
        if code == -1:
            error = com_const_error.CommonErrorType.UNEXCEPT_ERROR.value
    else:
        session.rollback()
        session.close()
    return error


if __name__ == '__main__':
    sys_log()
