#!/usr/bin/env python
# -*- coding:utf-8 -*- 
# --------------------
# Author:       SDN
# Description:  
# --------------------

from tornado.log import app_log

from base import AuthBaseModel
from utils.encrypt import md5


class LoginModel(AuthBaseModel):
    """登陆验证"""

    def check(self, name, pwd):
        """

        :param name: 用户名，公司工号
        :param pwd: 原始密码
        :return: 成功用户信息字典，没有或超过一条记录都为失败返回空字典
        """
        query_sql = 'select company_no from auth_user where company_no=%s and password=%s;'
        query_result = self.db_session.query(query_sql, *(name.upper(), md5(pwd)))
        # 数据库操作失败
        if query_result == -1:
            return {}
        # 数据库操作成功
        if len(query_result) == 1:
            return query_result[0]
        else:
            if len(query_result) > 1:
                app_log.error('user info is not unique!')
            else:
                app_log.error('user info is not right!')
            return {}


login_model = LoginModel()
