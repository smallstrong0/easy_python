# coding:utf-8

import os

import tornado.web
from tornado.options import define, options

# Options
define("port", default=7003, help="run on the given port", type=int)
define("debug", default=True, type=bool)
define("subpath", group='Webserver', type=str, default="/ss-api", help="Url subpath (such as /nebula)")
# define('unix_socket', group='Webserver', default=None, help='Path to unix socket to bind')
define('mysql', group='Webserver', type=str, default='', help='MySQL setting')
define('REDIS', group='Webserver', type=dict, default='', help='REDIS setting')
define('MNS', group='Webserver', type=tuple, default='', help='MNS setting')
define('ENVIRONMENT_AWARE', group='Webserver', type=str, default='', help='get_id')
tornado.options.parse_config_file('setting.py')

from url import urls

for u in urls:
    u[0] = options.subpath + u[0]
app = tornado.web.Application(
    handlers=urls,
    template_path=os.path.join(os.path.dirname(__file__), "template"),
    static_path=os.path.join(os.path.dirname(__file__), "static"),
    debug=True,
    allow_remote_access=True
)
