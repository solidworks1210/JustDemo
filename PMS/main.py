# -*- coding:utf-8 -*- 
# --------------------
# Author:       SDN
# Description:  主函数，项目入口
# --------------------

import tornado.options
from tornado import httpserver, ioloop, web
from tornado.log import app_log
from tornado.options import define, options

from configs import config
from configs import router

# 监听的端口
define("port", default=config.DEFAULT_PORT, help="default run port", type=int)
# 日志配置
options.log_file_prefix = config.LOG_SETTING['log_file_prefix']
options.logging = config.LOG_SETTING['logging']
options.log_to_stderr = config.LOG_SETTING['log_to_stderr']
options.log_file_max_size = config.LOG_SETTING['log_file_max_size']
options.log_file_num_backups = config.LOG_SETTING['log_file_num_backups']


# APP
class Application(web.Application):
    def __init__(self):
        # 路由
        handlers = router.HANDLERS
        # 配置
        settings = config.SETTINGS
        super(Application, self).__init__(handlers, **settings)


# Main入口
if __name__ == '__main__':
    # 监听命令栏输入
    tornado.options.parse_command_line()
    app_log.error('Starting system......')
    # 启动服务器线程
    http_server = httpserver.HTTPServer(
        Application(),
        xheaders=True,
        max_buffer_size=504857600,  # 文件上传使用
        max_body_size=504857600 # 文件上传使用
    )
    http_server.listen(options.port)
    app_log.error(
        'System start Success, listen on port: {0}, logging level: {1}'.format(options.port,
                                                                               config.LOG_SETTING['logging']))
    # 线程阻塞超过多长时间抛出异常，秒
    ioloop.IOLoop.current().set_blocking_log_threshold(1)
    # 启动服务
    ioloop.IOLoop.current().start()
