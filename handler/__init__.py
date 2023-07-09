#! /usr/bin/env python
# -*- coding: utf-8 -*-

# @Author: ss
# @Time: 2020/7/17 11:45 上午
# @File: __init__.py.py
import concurrent.futures
import time
from concurrent.futures import ThreadPoolExecutor

from apscheduler.executors import tornado
import tornado

ylc_thread_pool = concurrent.futures.ThreadPoolExecutor(
    thread_name_prefix='ylc',
    max_workers=50
)
