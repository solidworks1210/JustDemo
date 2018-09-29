#!/usr/bin/env python
# -*- coding:utf-8 -*- 
# --------------------
# Author:       SDN
# Description:  首页
# --------------------
from modules.common.handler.base import BaseHandler, check_login, check_auth


class IndexHandler(BaseHandler):

    @check_login()
    def get(self, *args, **kwargs):
        self.render_params['title'] = '首页'
        self.render_params['flags'] = self.get_flags(__name__)
        self.render('index.html', render_params=self.render_params)
