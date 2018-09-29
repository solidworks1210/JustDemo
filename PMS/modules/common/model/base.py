#!/usr/bin/env python
# -*- coding:utf-8 -*-
# --------------------
# Author:       SDN
# Description:  所有model的基类
# --------------------
import re

from configs import tables
from configs.config import DB
from utils.tornmq import Connection


class BaseModel(object):

    def __init__(self):
        # 数据库连接
        self.db_session = Connection(
            user=DB['user'], password=DB['pwd'],
            port=DB['port'], host=DB['host'], database=DB['db']
        )

    def get_user_info(self, company_no):
        """
        获取用户信息
        :param company_no:
        :return:
        """
        sql = "select * from {} where company_no=%s;".format(tables.USER)
        user_info = self.db_session.query(sql, company_no)
        if user_info == -1 or len(user_info) > 1 or len(user_info) == 0:
            return {}
        return user_info[0]


base_model = BaseModel()
