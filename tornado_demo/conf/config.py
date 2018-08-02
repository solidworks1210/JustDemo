# -*- coding:utf-8 -*-


import os.path

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
TEMPLATE_PATH = os.path.join(BASE_DIR, "templates")  # 模板目录
STATIC_PATH = os.path.join(BASE_DIR, "static")  # 静态资源目录

# Postgres配置
POSTGRES_HOST = "121.42.154.40"
# POSTGRES_HOST = "127.0.0.1"
POSTGRES_USER = "lcic"
POSTGRES_DB = "lcic_db"
POSTGRES_PWD = "CDMY@dt0504"
# POSTGRES_PWD = "123456"
POSTGRES_PORT = 5432

# Redis配置
REDIS_HOST = '127.0.0.1'
REDIS_PORT = 6379
REDIS_DB = 0
REDIS_URL = 'redis://@127.0.0.1:6379'

# tornado日志输出等级：debug < info < warning < error
LCIC_LOGGING_LEVEL = "info"
# 正式运行设为 True
LCIC_DEPLOY = False
# 默认端口
LCIC_DEFAULT_PORT = 9030
# 控制台是否输出日志: True 输出， False 不输出
LCIC_TERMINAL_SHOW_LOGGING = True

# SETTINGS
SETTINGS = dict(
    template_path=TEMPLATE_PATH,
    static_path=STATIC_PATH,
    cookie_secret="MmvPLn19QXqz83Pq3miVtUwYSA6oi0YCuUI26RUA/LU=",
    xsrf_cookies=True,
    login_url="/home/login",
    debug=False,
    ui_modules={}
)
