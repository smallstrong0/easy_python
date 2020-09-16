# -*- coding: utf-8 -*-


# Tornado imports
import tornado.auth
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.netutil
import tornado.web
import tornado.autoreload
import os, sys

from lib.scheduler_task.jobs import start_scheduler
from tornado.options import options
import logging.handlers

logging.basicConfig(stream=sys.stdout,
                    format='[%(asctime)s] - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s',
                    level=logging.DEBUG)


# Write your handlers here

def main():
    c = os.getcwd()
    from application import app
    options.logging = None
    #  解析命令行
    tornado.options.parse_command_line()
    options.subpath = options.subpath.strip('/')
    if options.subpath:
        options.subpath = '/' + options.subpath
        print(options.subpath)
    # 定时任务
    start_scheduler()
    io_loop = tornado.ioloop.IOLoop.instance()
    # Star application
    http_server = tornado.httpserver.HTTPServer(app, xheaders=True)
    # http_server.listen(options.port)
    http_server.listen(options.port, address="0.0.0.0")
    print('Server is running at http://127.0.0.1:%s' % options.port)
    print('Quit the server with Control-C')
    io_loop.start()


if __name__ == '__main__':
    main()
