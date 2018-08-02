# -*- coding:utf-8 -*-
# --------------------
# Author:		Ken
# Description:	公用基类
# --------------------

import tornado.web
from concurrent.futures import ThreadPoolExecutor


class BaseHandler(tornado.web.RequestHandler):
    # 一个线程池，用于将耗时请求异步化
    thread_pool = ThreadPoolExecutor(6)

    def data_received(self, chunk):
        """data_received no use"""

    def initialize(self):
        self.pageAttr = {"title": "", "pageflag": ""}

    def get_current_user(self):
        current_user = self.get_secure_cookie('user_name')
        if not current_user:
            return None
        return current_user

    def check_xsrf_cookie(self):
        pass

    def get_int_argument(self, arg_name, default=None):
        """
        将接收的参数转为int值
        :param default: 默认返回值
        :param arg_name: 参数名字
        :return:
        """
        try:
            return int(self.get_argument(arg_name))
        except:
            if default is not None:
                if not isinstance(default, int):
                    raise AttributeError('default value must be int')
                else:
                    return default
            else:
                raise AttributeError('value is not int str, or key not exist')
