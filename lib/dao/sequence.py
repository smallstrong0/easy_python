#!/bin/python
# -*- coding: utf8 -*-

import lib.common.func
from lib.common.redis_util import redis_client
from lib.common.redis_key import SequenceRedis

ID_QUEUE = 50000


def id():
    return id_obj.get_sequence_id()


def redis_id(num=1):
    day = int(lib.common.func.get_ts() / 86400)
    num = redis_client.incr_amount(SequenceRedis.SEQUENCE_ID.format(day), num)
    return int(str(day) + str(num).zfill(7))


class IdSequence:
    def __init__(self):
        self.sequence_id_list = [i for i in range(redis_id(1), redis_id(ID_QUEUE))]

    def get_sequence_id(self):
        if self.sequence_id_list:
            return self.sequence_id_list.pop(0)
        else:
            self.sequence_id_list = [i for i in range(redis_id(1), redis_id(ID_QUEUE))]
            return self.get_sequence_id()


id_obj = IdSequence()

if __name__ == "__main__":
    c = id()
    print(c)
