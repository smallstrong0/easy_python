#! /usr/bin/env python
# -*- coding: utf-8 -*-

# @Author: ss
# @Time: 2020/8/4 4:25 下午
# @File: redis_queue.py


import redis
from setting import REDIS
from lib.common.utils import serialize, deserialize


class RedisQueue(object):

    def __init__(self, queue_name):
        self.queue_name = queue_name
        self.__redis = redis.StrictRedis(host=REDIS['HOST'], port=REDIS['PORT'], password=REDIS['PASSWORD'],
                                         db=REDIS['DB'], socket_connect_timeout=5,
                                         socket_timeout=10, max_connections=10)

    def __len__(self):
        return self.__redis.llen(self.key)

    @property
    def key(self):
        return self.queue_name

    def clear(self):
        self.__redis.delete(self.key)

    def consume(self, **kwargs):
        kwargs.setdefault('block', True)
        kwargs.setdefault('timeout', 1)  # 默认阻塞 且超时一秒
        try:
            while True:
                msg = self.get(**kwargs)
                if msg is None:
                    break
                yield msg
        except Exception as e:
            print(e)
            return

    def get(self, block=False, timeout=None):
        if block:
            if timeout is None:
                timeout = 0
            msg = self.__redis.blpop(self.key, timeout=timeout)
            if msg is not None:
                msg = msg[1]
        else:
            msg = self.__redis.lpop(self.key)
        if msg is not None:
            msg = deserialize(msg)
        return msg

    def put(self, msg):
        self.__redis.rpush(self.key, serialize(msg))


if __name__ == '__main__':
    queue = RedisQueue(queue_name="bj:myqueue")
    queue.put({'a': 1})
    queue.put({'a': 1})
    queue.put({'a': 1})
    queue.put({'a': 1})
    queue.put({'a': 1})
    queue.put({'a': 1})
    queue.put({'a': 1})

    while 1:
        print(1111)
        for msg in queue.consume():
            print(msg)
