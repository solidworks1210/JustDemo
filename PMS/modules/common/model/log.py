#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author       : Ken
# --------------------
'''日志model'''

import queries
from tornado.log import app_log
from modules.common.model.base import BaseModel


class LogModel(BaseModel):
    '''日志记录'''

    def system_log(self, content, staff_id=0, staff_name='system'):
        '''系统日志'''
        try:
            result = self.pg_session.query(
                "INSERT INTO sy_system_log(content, staff_id, staff_name) VALUES (%(content)s,%(staff_id)s,%(staff_name)s) returning id",
                {
                    'content': content,
                    'staff_id': staff_id,
                    'staff_name': staff_name
                })
            self.pg_session.connection.commit()
            return result.as_dict()
        except queries.Error as ex:
            self.pg_session.connection.rollback()
            app_log.error(ex)


log_model = LogModel()
