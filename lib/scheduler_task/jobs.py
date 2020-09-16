from lib.scheduler_task import scheduler
from lib.scheduler_task.sys_api_log import sys_log
import datetime


def start_scheduler():
    # api日志队列
    scheduler.add_job(sys_log, 'interval', seconds=3600, next_run_time=datetime.datetime.now())
    scheduler.start()
