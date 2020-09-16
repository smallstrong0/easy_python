# coding=utf-8
import json

import redis
from setting import REDIS
import uuid
import time


class RedisClient:
    def __init__(self, host, password, port=6379, use_cache=True, db=0):
        """

        :param host:
        :param password:
        :param port:
        :param use_cache: 是否使用redis，传入False可以一键关闭缓存，可以用于对比测试
        """
        self.use_cache = use_cache
        try:
            self.session = redis.StrictRedis(host=host, port=port, password=password, db=db, socket_connect_timeout=5,
                                             socket_timeout=10, max_connections=10)
        except Exception as e:
            raise

    def set_str_cache(self, key, str, ex=60):
        """
        将内存数据二进制通过序列号转为文本流，再存入redis
        如果use_cache为False，表示不开启缓存，直接返回
        :param key: 缓存key，必须是str，且包含业务线，功能模块信息如
        supply-chain:user:info:100
        :param data: python对象不能
        :param ex: 缓存必须设置，默认60秒
        :return:
        """
        if not self.use_cache:
            return
        self.session.set(key, str, ex)

    def set_str_cache_no_ex(self, key, data):
        if not self.use_cache:
            return
        self.session.set(key, data)

    def get_str_cache(self, key):
        """
        将文本流从redis中读取并反序列化，返回
        如果use_cache为False，表示不开启缓存，直接返回
        :param key: 缓存key，必须是str
        :return:
        """
        if not self.use_cache:
            return None
        result = self.session.get(key)
        if result:
            result = bytes.decode(result)
        return result

    def delete_cache(self, key):
        if not self.use_cache:
            return None
        self.session.delete(key)

    # hash结构存储
    def set_hash_cache(self, name, redis_dict):
        if not self.use_cache:
            return
        self.session.hmset(name, redis_dict)

    def hset_hash_cache(self, name, key, value):
        if not self.use_cache:
            return
        return self.session.hset(name, key, value)

    # hash中key的vaule的自增
    def hincrby_hash_values(self, name, key, amount):
        if not self.use_cache:
            return
        self.session.hincrby(name, key, amount=amount)

    def get_hash_key(self, name, key):
        if not self.use_cache:
            return None
        result = self.session.hget(name, key)
        if result:
            result = bytes.decode(result)
        return result

    def delete_hash_cache(self, name):
        if not self.use_cache:
            return None
        keys = list(self.session.hkeys(name))
        if keys:
            result = self.session.hdel(name, *keys)
            return result

    def expireat_hash_cache(self, name, expire_time):
        if not self.use_cache:
            return
        self.session.expireat(name, expire_time)

    def setnx_cache(self, key, str):
        if not self.use_cache:
            return None
        result = self.session.setnx(key, str)
        return result

    def expire_cache(self, key, ex=60):
        if not self.use_cache:
            return None
        result = self.session.expire(key, ex)
        return result

    def zadd_zset_cache(self, name, mapping):
        '''点赞使用zset格式'''
        if not self.use_cache:
            return None
        return self.session.zadd(name, mapping)

    def zrem_zset_cache(self, name, member):
        if not self.use_cache:
            return None
        result = self.session.zrem(name, member)
        return result

    def zcart_zset_cache(self, name):
        if not self.use_cache:
            return None
        result = self.session.zcard(name)
        return result

    def zscore_zset_cache(self, name, member):
        if not self.use_cache:
            return None
        result = self.session.zscore(name, member)
        return result

    def incr(self, k):  # 集合元素的数量
        return self.session.incr(k)

    def get_all_keys(self, name):
        if not self.use_cache:
            return None
        result = self.session.keys(pattern=name + '*')
        if result:
            result = [bytes.decode(i) for i in result]
        return result

    def incrby(self, k, amount):
        return self.session.incrby(k, amount)

    def decrby(self, k, amount):
        return self.session.decrby(k, amount)

    def acquire_lock(self, lock_name, acquire_time=5, time_out=5):
        """获取一个分布式锁"""
        identifier = str(uuid.uuid4())
        end = time.time() + acquire_time
        lock = "string:lock:" + lock_name
        while time.time() < end:
            if self.session.setnx(lock, identifier):
                # 给锁设置超时时间, 防止进程崩溃导致其他进程无法获取锁
                self.session.expire(lock, time_out)
                return identifier
            elif not self.session.ttl(lock):
                self.session.expire(lock, time_out)
            time.sleep(0.2)
        return False

    # 释放一个锁
    def release_lock(self, lock_name, identifier):
        """通用的锁释放函数"""
        lock = "string:lock:" + lock_name
        pip = self.session.pipeline(True)
        while True:
            try:
                pip.watch(lock)
                lock_value = self.session.get(lock)
                if not lock_value:
                    return True

                if lock_value.decode() == identifier:
                    pip.multi()
                    pip.delete(lock)
                    pip.execute()
                    return True
                pip.unwatch()
                break
            except redis.exceptions.WatchError:
                pass
        return False


redis_client = RedisClient(host=REDIS['HOST'], password=REDIS['PASSWORD'], port=REDIS['PORT'],
                           use_cache=REDIS['USE_REDIS_CACHE'], db=REDIS['DB'])
