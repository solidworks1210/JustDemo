#!/usr/bin/env python
# -*- coding:utf-8 -*- 
# --------------------
# Author:       SDN
# Description:  用户管理
# --------------------
from modules.auth.model.user import user_model
from modules.common.handler.base import BaseHandler, check_login, check_auth


class UserHandler(BaseHandler):

    @check_login()
    @check_auth("modules.auth.handler.user.UserHandler.get")
    def get(self):
        """获取所有用户的列表"""
        self.render_params['title'] = '用户管理'
        self.render_params['flags'] = self.get_flags(__name__)
        self.render_params['items'] = user_model.get_users()
        self.render('user.html', render_params=self.render_params)

    @check_login()
    @check_auth("modules.auth.handler.user.UserHandler.get")
    def post(self):
        """添加用户"""
        name = self.get_argument('name', strip=True)
        pwd = self.get_argument('pwd', strip=True)
        # todo: 添加用户时，输入信息验证
        result = user_model.add_user(name, pwd)
        if result == -1:
            self.write({'status': 0, 'msg': '添加用户失败', 'result': {}})
        else:
            self.write({'status': 1, 'msg': '成功添加用户', 'result': {}})


class UserProfileHandler(BaseHandler):
    @check_login()
    @check_auth("modules.auth.handler.user.UserProfileHandler.get")
    def get(self, user_id):
        """获取某个用户的信息"""
        self.render_params['title'] = '用户管理'
        self.render_params['flags'] = self.get_flags(__name__)
        self.render('user_profile.html', render_params=self.render_params)

    def put(self, user_id):
        """修改用户信息"""
        pass

    @check_login()
    @check_auth("modules.auth.handler.user.UserProfileHandler.delete")
    def delete(self, user_id):
        """删除用户"""
        result = user_model.delete(user_id)
        if result == -1:
            self.write({'status': 0, 'msg': '删除用户失败', 'result': {}})
        else:
            self.write({'status': 1, 'msg': '成功删除用户', 'result': {}})
