# -*- coding:utf-8 -*- 
# --------------------
# Author:       SDN
# Description:	自定的
# Time:         2017/3/1
# --------------------
import functools

from tornado.web import HTTPError


def authenticated(method):
    """
    自定义的@tornado.web.authenticated
    """
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        if not self.current_user:
            if self.request.method in ("GET", "HEAD"):

                self.redirect('/manage/login')
                return
            raise HTTPError(403)
        return method(self, *args, **kwargs)
    return wrapper
