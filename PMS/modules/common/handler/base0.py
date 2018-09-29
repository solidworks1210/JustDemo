#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author       :
# --------------------
'''基类handler'''

import functools
import json
from datetime import datetime, date
from tornado import web

# this decorator can only decorate a RequestHandler subclass
from modules.common.model.base import base_model


def has_auth(key):
    """用户权限验证"""

    def check_auth(method):
        @functools.wraps(method)
        def wrapper(self, *args, **kwargs):
            if not self.has_auth(key):
                # self.write({"state":state.KEY[0],"msg":state.KEY[1],"result":{}})
                self.redirect("/error?error_message=您没有权限进行该操作")
                return
            return method(self, *args, **kwargs)

        return wrapper

    return check_auth


# this decorator can only decorate a RequestHandler subclass
def check_admin_login(method):
    """与tornado.web.authenticated作用相同，因前端、后端登陆验证需要分开判断，故加此法"""

    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        if not self.check_admin_login():
            self.redirect("/admin/login")
            return
        return method(self, *args, **kwargs)

    return wrapper


class BaseHandler(web.RequestHandler):
    ''' BaseHandler '''

    def initialize(self):
        # 默认页面信息
        self.pageAttr = {
            "title": "",
            "flag": "",
            "father_flag": "",
            'setting': base_model.get_basic_info()
        }

    def has_auth(self, key):
        """后台权限验证"""
        return self.current_user and key in self.current_user['permission_list']

    def check_admin_login(self):
        """后台登录验证"""
        admin_info = self.get_secure_cookie('admininfo')
        if not admin_info:
            return None
        else:
            admin_obj = json.loads(admin_info)
            return admin_obj

    def data_received(self, chunk):
        pass

    def get_current_user(self):
        """
        用户登陆验证(前台使用), 与setting中的login_url配合tornado.web.authenticated
        :return:
        """
        user_info = self.get_secure_cookie('userinfo')
        if not user_info:
            return None
        else:
            user_obj = json.loads(user_info)
            return user_obj

    def check_xsrf_cookie(self):
        """check_xsrf_cookie"""
        pass  # for test

    def get_int_argument(self, name_args, default_value=None):
        """
        将前端传来的数据转为整数
        :param name_args: 前端传递参数的名字
        :param default_value: 参数不存在，返回的默认值
        :return:
        """
        try:
            result_temp = self.get_argument(name_args, strip=True)
            return int(result_temp)
        except:
            if default_value is not None:
                if isinstance(default_value, type(1)):
                    return default_value
                else:
                    raise TypeError('default value is not int')
            else:
                raise TypeError('default value is not given')

    def get_float_argument(self, name_args, default_value=None):
        """
        将前端传来的数据转为float
        :param name_args: 前端传递参数的名字
        :param default_value: 参数不存在，返回的默认值
        :return:
        """
        try:
            result_temp = self.get_argument(name_args, strip=True)
            return float(result_temp)
        except:
            if default_value is not None:
                if isinstance(default_value, type(0.1)):
                    return default_value
                else:
                    raise TypeError('default value is not float')
            else:
                raise TypeError('default value is not given')

    @staticmethod
    def to_json(obj):
        """
        将字典对象转为json对象（日期对象转字符串）
        :param obj:
        :return:
        """
        return json.dumps(obj, ensure_ascii=False, cls=CJsonEncoder)


class CJsonEncoder(json.JSONEncoder):
    """json dumps时，日期和时间格式化"""

    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        else:
            try:
                iterable = iter(obj)
            except TypeError:
                pass
            else:
                return list(iterable)
