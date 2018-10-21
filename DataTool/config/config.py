# -*- coding:utf-8 -*-
# --------------------
# Author:       SDN
# Description:	基本配置
# Time:         2017/2/28
# --------------------

import os

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'db', 'data_tool.sqlite')

# 后台安全cookie名
H_SECRETE_COOKIE = 'hfc'

# 前台安全cookie名
Q_SECRETE_COOKIE = 'qfc'

# 验证码 cookie名
Q_VERIFY = 'cfc'

# 数据库
HOST = '127.0.0.1'
PORT = 3306
USER = 'root'
PASSWORD = 'password'
DATABASE = 'tool'

# Application
SETTING = dict(
    template_path=os.path.join(os.path.dirname(os.path.dirname(__file__)), 'templates'),
    static_path=os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static'),
    cookie_secret='8l35cIieQw2C1HqSqwde9qtXQ5haBEBJu0f4nZJI/cM=',
    xsrf_cookies=True,
    login_url=r'/login',  # 后台用
    debug=False,
    ui_modules={

    },
)
