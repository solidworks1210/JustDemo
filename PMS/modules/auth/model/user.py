#!/usr/bin/env python
# -*- coding:utf-8 -*- 
# --------------------
# Author:       SDN
# Description:  
# --------------------
from configs import tables, constant
from modules.common.model.base import BaseModel
from utils.encrypt import md5


class UserModel(BaseModel):
    def add_user(self, name, pwd):
        """添加用户"""
        return self.db_session.insert_one(tables.USER, **{'company_no': name.upper(), 'password': md5(pwd)})

    def get_users(self, **kwargs):
        """
        获取用户列表
        :param kwargs:
        :return:
        """
        sql = "select company_no, sex from {};".format(tables.USER)
        result = self.db_session.query(sql)
        for item in result:
            item['sex'] = constant.SEX_NAME.get(item['sex'], u'未知')
        return result

    def get(self, user_id):
        """获取用户的详细信息"""
        pass

    def update(self, user_id, **kwargs):
        """更新用户信息"""
        pass

    def delete(self, user_id):
        """删除用户"""
        return self.db_session.delete_one(tables.USER, **{'company_no': user_id.upper()})


user_model = UserModel()
