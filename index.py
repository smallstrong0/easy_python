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
import asyncio
from tornado.options import define, options, parse_command_line
import logging.handlers
from handler.base import APINotFoundHandler
from url import urls
import uvloop
asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

# 配置优先级
'''
1.外部传入  ( python index.py --port=3333)
2.setting.py 设置
3.index.py 默认值
'''
define('env', default='test', help='env setting', type=str)
define("port", default=1111, help="run on the given port", type=int)
define("debug", default=True, help="run in debug mode", type=bool)
define("subpath", default='ss', help="url subpath", type=str)
tornado.options.parse_config_file('setting.py')
logging.basicConfig(stream=sys.stdout,
                    format='[%(asctime)s] - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s',
                    level=logging.DEBUG)


async def main():
    parse_command_line()
    urls.append([r'.*', APINotFoundHandler])
    for u in urls:
        u[0] = '/' + options.subpath + u[0]
    print(urls)
    app = tornado.web.Application(
        handlers=urls,
        template_path=os.path.join(os.path.dirname(__file__), "templates"),
        static_path=os.path.join(os.path.dirname(__file__), "static"),
        debug=options.debug,
        allow_remote_access=True
    )
    app.listen(port=options.port, address="0.0.0.0")
    print('Server is running at http://127.0.0.1:%s' % options.port)
    print('Quit the server with Control-C')
    await asyncio.Event().wait()


if __name__ == '__main__':
    asyncio.run(main())
