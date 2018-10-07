# -*- coding:utf-8 -*-

import tornado.options
import tornado.web
import tornado.httpserver
import tornado.ioloop

from config.router import HANDLERS
from config.config import SETTING
from tornado.log import app_log

tornado.options.define('port', default=8080, type=int)


class MyApplication(tornado.web.Application):
    def __init__(self):
        handlers = HANDLERS
        setting = SETTING
        tornado.web.Application.__init__(self, handlers=handlers, **setting)


if __name__ == '__main__':
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(MyApplication())
    app_log.info('Listen port %s......' % tornado.options.options.port)
    http_server.listen(tornado.options.options.port)
    tornado.ioloop.IOLoop.current().start()
