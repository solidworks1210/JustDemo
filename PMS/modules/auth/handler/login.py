#!/usr/bin/env python
# -*- coding:utf-8 -*-
# --------------------
# Author:       SDN
# Description:  用户登陆、登出管理
# --------------------

from configs.config import SECURE_COOKIE_AUTH
from modules.auth.model.login import login_model
from modules.common.handler.base import BaseHandler, check_login


class LoginHandler(BaseHandler):
    """用户登陆"""

    def get(self, *args, **kwargs):
        if self.current_user:
            # self.redirect('/')
            self.redirect('/share')
            return
        self.render('login.html')

    def post(self, *args, **kwargs):
        """登陆验证"""
        name = self.get_argument('name', strip=True)
        pwd = self.get_argument('pwd', strip=True)
        user_info = login_model.check(name=name, pwd=pwd)
        if not user_info:
            self.write({
                "state": 0,
                "msg": '',
                "result": {}
            })
        else:
            # 后台用户cookie，用于判断后台是否登录（把验证信息放在cookie中）
            self.set_secure_cookie(
                SECURE_COOKIE_AUTH, self.to_json(user_info), expires_days=None)
            self.write({
                "state": 1,
                "msg": '',
                "result": {}
            })


class LogoutHandler(BaseHandler):
    """用户登出"""

    @check_login()
    def put(self, *args, **kwargs):
        self.clear_cookie(SECURE_COOKIE_AUTH)
