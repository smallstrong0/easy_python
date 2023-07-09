#! /usr/bin/env python
# -*- coding: utf-8 -*-
from apscheduler.schedulers.tornado import TornadoScheduler
from apscheduler.executors.tornado import TornadoExecutor

MAX_EXECUTOR = 100  # 任务最多进程数量
executors = {
    'default': TornadoExecutor(MAX_EXECUTOR)
}

scheduler = TornadoScheduler()
scheduler._executors = executors
