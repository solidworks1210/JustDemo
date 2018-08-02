# -*- coding:utf-8 -*- 

import tornado.options
from tornado import httpserver, ioloop, web
from tornado.log import app_log
from tornado.options import define, options

from conf.config import SETTINGS, LCIC_LOGGING_LEVEL, LCIC_TERMINAL_SHOW_LOGGING, LCIC_DEFAULT_PORT
from router import HANDLERS

# 监听的端口
define("port", default=LCIC_DEFAULT_PORT, help="default run port", type=int)
# 日志文件名
define("log_file_prefix", default="lcic.log", help="log file prefix")
# 配置日志输出级别
options.logging = LCIC_LOGGING_LEVEL
# 控制台是否显示日志
options.log_to_stderr = LCIC_TERMINAL_SHOW_LOGGING


# APP
class Application(web.Application):
    def __init__(self):
        # 路由
        handlers = HANDLERS
        # 配置
        settings = SETTINGS
        super(Application, self).__init__(handlers, **settings)


# Main入口
if __name__ == '__main__':
    # 监听命令栏输入
    tornado.options.parse_command_line()
    app_log.error('Starting system......')
    # 启动服务器线程
    http_server = httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    app_log.error('>--- Success, listen on port: {0}, logging level: {1} ---<'.format(options.port, LCIC_LOGGING_LEVEL))
    # 线程阻塞超过多长时间抛出异常，秒
    # ioloop.IOLoop.current().set_blocking_log_threshold(1)
    # 启动服务
    ioloop.IOLoop.current().start()
