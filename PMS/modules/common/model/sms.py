#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author       : Ken
# --------------------
'''短信model'''

import queries
from tornado.log import app_log
from modules.common.model.base import BaseModel


class SmsModel(BaseModel):
    '''短信发送记录'''

    def add_smscode(self, type, userid, phone, content, status):
        '''验证码发送记录，寻程平台---验证码'''
        try:
            result = self.pg_session.query(
                """INSERT INTO sys_sms(type,userid,phone,content,status,send_time,create_time) 
                VALUES(%(type)s,%(userid)s,%(phone)s,%(content)s,%(status)s,now(),now()) returning id""",
                {
                    "type": type,
                    'userid': userid,
                    'phone': phone,
                    'content': content,
                    'status': status
                })
            self.pg_session.connection.commit()
            return result.as_dict()
        except queries.Error as ex:
            self.pg_session.connection.rollback()
            app_log.error(ex)

    def add_sms_queen(self, sms_tuple):
        '''验证码发送，非寻程平台'''
        try:
            self.pg_session.connection.cursor().executemany(
                'INSERT INTO sys_sms(type,userid,phone,content,status,create_time) VALUES(%s,%s,%s,%s,%s,now())',
                sms_tuple)
            return True
        except queries.Error as ex:
            app_log.error(ex)

sms_model = SmsModel()
