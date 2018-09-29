#!/usr/bin/env python
# -*- coding:utf-8 -*-
# --------------------
# Author:       SDN
# Description:  基类handler
# --------------------

import functools
import json
import urlparse
from datetime import datetime, date
from urllib import urlencode

from concurrent.futures import ThreadPoolExecutor
from tornado import web

from configs.config import REDIRECT_URL, SECURE_COOKIE_AUTH, LOGIN_URL
from modules.common.model.base import base_model


def check_auth(key, redirect_url=REDIRECT_URL):
    """
    用户权限验证
    :param key: 权限验证key
    :param redirect_url: 权限验证失败跳转的页面
    :return:
    """

    def check(method):
        @functools.wraps(method)
        def wrapper(self, *args, **kwargs):
            # if not self.has_auth(key):
            #     if self.request.method in ("GET", "HEAD"):
            #         self.redirect(redirect_url)
            #     else:
            #         self.write({"state": 0, "msg": u'无权限', "result": {}})
            #     return
            return method(self, *args, **kwargs)

        return wrapper

    return check


def check_login(redirect_url=LOGIN_URL):
    """
    登陆验证, 参考自tornado的authenticated，增加自定义重定向连接
    :param redirect_url:
    :return:
    """

    def check(method):
        @functools.wraps(method)
        def wrapper(self, *args, **kwargs):
            if not self.current_user:
                if self.request.method in ("GET", "HEAD"):
                    url = redirect_url
                    if "?" not in url:
                        if urlparse.urlsplit(url).scheme:
                            # if login url is absolute, make next absolute too
                            next_url = self.request.full_url()
                        else:
                            next_url = self.request.uri
                        url += "?" + urlencode(dict(next=next_url))
                    self.redirect(url)
                else:
                    self.write({"state": 0, "msg": u'登陆验证失败', "result": {}})
                return
            return method(self, *args, **kwargs)

        return wrapper

    return check


class BaseHandler(web.RequestHandler):
    """所有handler的基类"""
    thread_pool = ThreadPoolExecutor(6)

    def initialize(self):
        # 默认页面信息
        self.render_params = {
            "title": "",
            "flags": [],  # flag list，从大到小排序：flag1, flag2,...
            "user_info": self.current_user,
            # 'setting': base_model.get_basic_info()
        }

    def write_error(self, status_code, **kwargs):
        """请求出错返回的内容，统一在这儿操作：请求异常，后台出错"""
        self.write('这是自定义错误页面<br>')
        self.write('status_code:%s' % status_code)

    def data_received(self, chunk):
        pass

    def get_current_user(self):
        """
        用户登陆验证(前台使用), 与setting中的login_url配合tornado.web.authenticated
        这儿获取的cook在登陆时放入
        :return:
        """
        user_info = self.get_secure_cookie(SECURE_COOKIE_AUTH)
        if not user_info:
            return None
        else:
            user_obj = json.loads(user_info)
            company_no = user_obj['company_no']
            user_info = base_model.get_user_info(company_no)
            if user_info:
                return user_info
            else:
                return None

    # def check_xsrf_cookie(self):
    #     """xsrf_cookies 为 True，这个方法要注释掉"""
    #     pass  # for test

    def has_auth(self, key):
        """权限验证"""
        return self.current_user and key in self.current_user['permission_list']

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

    @classmethod
    def get_flags(cls, module_name, *args):
        """
        生成导航标签
        :param module_name: __name__
        :param args: 多级导航时使用
        :return: [flag0, flag1, ...]
        """

        flag0 = module_name
        flag1 = module_name + '.' + cls.__name__
        flag_n = []
        for index, item in enumerate(args):
            print index, item
            if index == 0:
                flag_n.append(flag1 + '.' + str(item))
            else:
                flag_n.append(flag_n[index - 1] + '.' + str(item))
        result = [flag0] + [flag1] + flag_n
        return result


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
