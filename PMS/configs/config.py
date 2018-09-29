#!/usr/bin/env python
# -*- coding:utf-8 -*-
# --------------------
# Author:       SDN
# Description:  项目通用的配置
# --------------------

import os.path

# 默认端口
DEFAULT_PORT = 9030

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
TEMPLATE_PATH = os.path.join(BASE_DIR, "templates")  # 模板目录
STATIC_PATH = os.path.join(BASE_DIR, "statics")  # 静态资源目录

# 数据库配置
DB = dict(
    host="127.0.0.1",
    user="root",
    db="pms",
    pwd="password",
    port=3306
)

# 日志配置
LOG_SETTING = dict(
    # tornado日志输出等级：debug < info < warning < error,
    logging="info",
    # 日志保存路径：多个tornado实列时，要在启动项目时指定该参数，以区分
    log_file_prefix=os.path.join(BASE_DIR, 'logs/pms.log'),
    # 控制台是否显示日志
    log_to_stderr=True,
    # 日志文件大小
    log_file_max_size=100 * 1000 * 1000,
    # 日志文件保存的个数
    log_file_num_backups=5
)

# SETTINGS
SETTINGS = dict(
    # 模板文件在项目中路径（相对与项目根路径）
    template_path=TEMPLATE_PATH,
    # 静态文件在项目中路径（相对与项目根路径）
    static_path=STATIC_PATH,
    # 项目中的静态文件都是用{{ static_url('') }}，如果href="/xx/css/index.css"，就必须保证xx与这儿配置的同
    static_url_prefix="/statics/",
    # 安全cook
    cookie_secret="MmvPLn19QXqz83Pq3miVtUwYSA6oi0YCuUI26RUA/LU=",
    # 启用xsrf安全控制，需在handler中实现：def check_xsrf_cookie(self):
    xsrf_cookies=True,
    # 登陆验证，需要handler中实现：def get_current_user(self):
    login_url="/login",
    # 开启测试模式，修改python代码会自动重启项目
    debug=False,
    ui_modules={}
)

# cookie名字
SECURE_COOKIE_AUTH = 'user_info'

# 权限验证失败跳转的页面
REDIRECT_URL = u"/error?error_message=您没有权限进行该操作"
# 登陆验证失败跳转的页面
LOGIN_URL = "/login"
