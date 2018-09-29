#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author       : Ken
# --------------------
'''短信验证类'''

import random
import time
import json
import traceback

from concurrent.futures import ThreadPoolExecutor
from tornado.concurrent import run_on_executor
import tornado
from tornado.log import app_log
from modules.common.handler.base import BaseHandler
from modules.common.model.sms import sms_model
from modules.home.model.user import user_model
from conf import state
from utils.sms_push import apistoreSMS
from utils.redis_utils import redis_manager


class GetSmsCodeHandler(BaseHandler):
    '''获取验证码'''

    executor = ThreadPoolExecutor(2048)

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def post(self, *args, **kwargs):
        # 验证码类型，register-注册，reset-找回密码
        sms_type = self.get_argument("sms_type", "register").encode("utf-8")
        phone = self.get_argument("phone", "").encode("utf-8")

        # 验证手机号格式
        if len(phone) != 11:
            result = {
                "state": state.WEB_ERROR_PARAMS[0],
                "msg": state.WEB_ERROR_PARAMS[1],
                "result": {}
            }
            self.write(result)
            return

        user_obj = user_model.exist(phone)

        # 注册验证码
        if sms_type == 'register':
            if user_obj:
                result = {
                    "state": state.WEB_ERROR_HASPHONE[0],
                    "msg": state.WEB_ERROR_HASPHONE[1],
                    "result": {}
                }
                self.write(result)
            else:
                yield self.sendcode(0, phone)

        # 找回密码，需验证手机号是否存在
        if sms_type == 'reset':
            if user_obj:
                yield self.sendcode(user_obj['id'], phone)
            else:
                result = {
                    "state": state.WEB_ERROR_NOPHONE[0],
                    "msg": state.WEB_ERROR_NOPHONE[1],
                    "result": {}
                }
                self.write(result)

    @run_on_executor
    def sendcode(self, userid, phone):
        '''发送短信'''

        result = {
            "state": state.WEB_ERROR_UNDEFINED[0],
            "msg": state.WEB_ERROR_UNDEFINED[1],
            "result": {}
        }

        try:

            # 取验证码
            smscode_obj = redis_manager.hget("smscode", phone)
            # 已存在
            if smscode_obj:

                smscode_obj = json.loads(smscode_obj)
                past_time = int(time.time()) - smscode_obj['create_time']
                # 1分钟只发一次
                if int(time.time()) - smscode_obj['update_time'] < 60:
                    result = {
                        "state": state.WEB_ERROR_TOOMUCH[0],
                        "msg": state.WEB_ERROR_TOOMUCH[1],
                        "result": {}
                    }
                # 已过期，清空缓存，待重发
                elif past_time > 3600:
                    redis_manager.hdel("smscode", phone)
                # 未过期，重发一次
                else:
                    # 修改上次发送时间
                    smscode_obj['update_time'] = int(time.time())

                    # 保存新的对象
                    redis_manager.hset("smscode", phone,
                                       json.dumps(smscode_obj))

                    # 封装内容
                    content = "【宴语】您本次的验证码为：" + str(
                        smscode_obj['smscode']) + "，有效期为60分钟。"

                    #发送短信
                    ret = apistoreSMS(phone, content)

                    # 封装返回值
                    ret_obj = json.loads(ret)
                    status = 0
                    if ret_obj and ret_obj['error_code'] == 0:
                        result = {
                            "state": state.WEB_SUCCESS[0],
                            "msg": state.WEB_SUCCESS[1],
                            "result": {}
                        }
                        status = 1
                    else:
                        result = {
                            "state": state.WEB_FAIL[0],
                            "msg": state.WEB_FAIL[1],
                            "result": {}
                        }
                        status = 2
                    # 回写短信表
                    sms_model.add_smscode(0, userid, phone, content, status)

            # 重新生成验证码并缓存
            if not redis_manager.hget("smscode", phone):
                # 生成随机码
                smscode = str(random.randint(100000, 999999))

                # 封装对象并保存
                smscode_obj = {
                    "smscode": smscode,
                    "create_time": int(time.time()),
                    "update_time": int(time.time())
                }
                redis_manager.hset("smscode", phone, json.dumps(smscode_obj))

                # 封装内容
                content = "【宴语】您本次的验证码为：" + str(
                    smscode_obj['smscode']) + "，有效期为60分钟。"

                # 发送短信
                ret = apistoreSMS(phone, content)

                # 封装返回值
                ret_obj = json.loads(ret)
                status = 0
                if ret_obj and ret_obj['error_code'] == 0:
                    result = {
                        "state": state.WEB_SUCCESS[0],
                        "msg": state.WEB_SUCCESS[1],
                        "result": {}
                    }
                    status = 1
                else:
                    result = {
                        "state": state.WEB_FAIL[0],
                        "msg": state.WEB_FAIL[1],
                        "result": {}
                    }
                    status = 2

                # 回写短信表
                sms_model.add_smscode(0, userid, phone, content, status)
        # 为了保证线程正常结束，异常捕获的范围比较大
        except Exception as ex:
            app_log.error(ex)
        self.write(result)


class CheckSmsCodeHandler(BaseHandler):
    '''提交验证码'''

    def post(self, *args, **kwargs):

        result = {
            "state": state.WEB_ERROR_UNDEFINED[0],
            "msg": state.WEB_ERROR_UNDEFINED[1],
            "result": {}
        }

        phone = self.get_argument("phone", "").encode("utf-8")
        smscode = self.get_argument("smscode", "").encode("utf-8")

        if len(phone) != 11 or len(smscode) != 6:
            result = {
                "state": state.WEB_ERROR_PARAMS[0],
                "msg": state.WEB_ERROR_PARAMS[1],
                "result": {}
            }
        else:
            # 取验证码
            old_smscode = redis_manager.hget("smscode", phone)
            if old_smscode:
                old_smscode = json.loads(old_smscode)

            if old_smscode and old_smscode['smscode'] == smscode:
                result = {
                    "state": state.WEB_SUCCESS[0],
                    "msg": state.WEB_SUCCESS[1],
                    "result": {}
                }
                # 销毁验证码
                redis_manager.hdel("smscode", phone)
            else:
                result = {
                    "state": state.WEB_ERROR_SMSCODE[0],
                    "msg": state.WEB_ERROR_SMSCODE[1],
                    "result": {}
                }

        self.write(result)
