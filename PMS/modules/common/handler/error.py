#!/usr/bin/env python
# -*- coding:utf-8 -*-
# --------------------
# Author:       SDN
# Description:  错误跳转页面
# --------------------
from modules.common.handler.base import BaseHandler


class AuthErrorHandler(BaseHandler):
    """权限验证失败跳转的页面"""

    def get(self, *args, **kwargs):
        error_message = self.get_argument("error_message",
                                          "未知错误").encode("utf-8")

        self.pageAttr["title"] = "出错了"
        self.pageAttr["flag"] = "modules.common.handler.error.ErrorHandler"
        self.render(
            'admin/error.html',
            pageAttr=self.pageAttr,
            error_message=error_message)


class NotFoundHandler(BaseHandler):
    """未定义路由处理"""

    def get(self, *args, **kwargs):
        # self.send_error(404)
        self.write('接口不存在')

    # def write_error(self, status_code, **kwargs):
    #     self.render('error.html')
