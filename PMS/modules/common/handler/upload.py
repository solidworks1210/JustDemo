#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author       : Ken
# --------------------
'''文件上传类'''

import os
import json
import tornado
from tornado.log import app_log
from tornado.concurrent import futures, run_on_executor
from tornado.web import authenticated
from conf import state
from utils.file import hand_photo
from utils import excel
from modules.common.handler.base import BaseHandler


class UploadHandler(BaseHandler):
    '''文件上传处理'''

    executor = futures.ThreadPoolExecutor(2048)

    @authenticated
    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def post(self, *args, **kwargs):
        utype = self.get_argument('utype', 'normal').encode('UTF-8')
        post_data = {}
        for key in self.request.arguments:
            post_data[key] = self.get_arguments(key)
        if utype == 'excel':
            yield self.savexcel()
        elif utype == 'icloud':
            yield self.saveicloud()
        else:
            yield self.savenormal()

    @run_on_executor
    def savenormal(self):
        '''保存图片'''
        width = int(self.get_argument('width', 500))
        height = int(self.get_argument('height', 500))
        quality = int(self.get_argument('quality', 80))

        #取NGINX传来的文件参数
        file_name = self.get_argument('last-calls_name', 'uploaded.file')
        file_content_type = self.get_argument('last-calls_content_type', "")
        # file_size = self.get_argument('file_size', -1)
        file_md5 = self.get_argument('last-calls_md5', '')
        file_path = self.get_argument('last-calls_path', '').encode('UTF-8')

        # 基础信息验证
        if len(file_name) < 1 or len(file_content_type) < 1 or len(
                file_md5) < 6 or len(file_path) < 1:
            if len(file_path) > 1:
                os.remove(file_path)
            self.write({
                "state": state.API_FAIL[0],
                "msg": state.API_FAIL[1],
                "result": {}
            })
            return
        #判断文件类型
        if not file_content_type or (file_content_type != "image/jpeg" and
                                     file_content_type != "image/png"):
            os.remove(file_path)
            self.write({
                "state": state.API_ERROR_FILE_FORMANT[0],
                "msg": state.API_ERROR_FILE_FORMANT[1],
                "result": {}
            })
            return
        tmp_file_path = hand_photo(file_md5, file_path, width, height, quality)

        if tmp_file_path:
            new_file_name = os.path.basename(tmp_file_path)
            ret_path = os.path.join("/static/upload/tmp", new_file_name)
            self.write({
                "state": state.WEB_SUCCESS[0],
                "msg": state.WEB_SUCCESS[1],
                "result": ret_path
            })

        else:
            self.write({
                "state": state.WEB_FAIL[0],
                "msg": state.WEB_FAIL[1],
                "result": {}
            })

    @run_on_executor
    def savexcel(self):
        '''保存文件'''

        #取NGINX传来的文件参数
        file_name = self.get_argument('last-calls_name', 'uploaded.file')
        file_content_type = self.get_argument('last-calls_content_type', "")
        # file_size = self.get_argument('file_size', -1)
        file_md5 = self.get_argument('last-calls_md5', '')
        file_path = self.get_argument('last-calls_path', '').encode('UTF-8')

        # 基础信息验证
        if len(file_name) < 1 or len(file_content_type) < 1 or len(
                file_md5) < 6 or len(file_path) < 1:
            if len(file_path) > 1:
                os.remove(file_path)
            self.write({
                "state": state.WEB_FAIL_PARAMS[0],
                "msg": state.WEB_FAIL_PARAMS[1],
                "result": {}
            })
            return
        #判断文件类型
        if not file_content_type or (
                file_content_type !=
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                and file_content_type != "application/octet-stream"):
            os.remove(file_path)
            self.write({
                "state": state.WEB_ERROR_FILE_FORMANT[0],
                "msg": state.WEB_ERROR_FILE_FORMANT[1],
                "result": {}
            })
            return
        calls_tuples = excel.read_excel_tuple(file_path)
        try:
            os.remove(file_path)
        except IOError as ex:
            app_log(ex)
        if calls_tuples:

            timeStartIndex = -1
            calltimeIndex = -1
            callTypeIndex = -1
            phoneIndex = -1
            localAddIndex = -1
            desAddIndex = -1

            if calls_tuples[0].count("通话起始时间") > 0:
                timeStartIndex = calls_tuples[0].index("通话起始时间")
            if calls_tuples[0].count("通话时长") > 0:
                calltimeIndex = calls_tuples[0].index("通话时长")
            if calls_tuples[0].count("呼叫类型") > 0:
                callTypeIndex = calls_tuples[0].index("呼叫类型")
            if calls_tuples[0].count("对方号码") > 0:
                phoneIndex = calls_tuples[0].index("对方号码")
            if calls_tuples[0].count("本机通话地") > 0:
                localAddIndex = calls_tuples[0].index("本机通话地")
            if calls_tuples[0].count("对方归属地") > 0:
                desAddIndex = calls_tuples[0].index("对方归属地")

            if timeStartIndex < 0 or calltimeIndex < 0 or callTypeIndex < 0 or phoneIndex < 0 or localAddIndex < 0 or desAddIndex < 0:
                self.write({
                    "state": state.WEB_FAIL[0],
                    "msg": "格式错误",
                    "result": calls_tuples
                })
                return

            calls = []
            del calls_tuples[0]
            for row in calls_tuples:
                new_row = (row[timeStartIndex], row[calltimeIndex],
                           row[callTypeIndex], row[phoneIndex],
                           row[localAddIndex], row[desAddIndex])
                calls.append(new_row)

            self.write({
                "state": state.WEB_SUCCESS[0],
                "msg": state.WEB_SUCCESS[1],
                "result": calls
            })
        else:
            self.write({
                "state": state.WEB_FAIL[0],
                "msg": state.WEB_FAIL[1],
                "result": {}
            })

    @run_on_executor
    def saveicloud(self):
        '''保存icloud'''

        #取NGINX传来的文件参数
        file_name = self.get_argument('last-calls_name', 'uploaded.file')
        file_content_type = self.get_argument('last-calls_content_type', "")
        # file_size = self.get_argument('file_size', -1)
        file_md5 = self.get_argument('last-calls_md5', '')
        file_path = self.get_argument('last-calls_path', '').encode('UTF-8')

        # 基础信息验证
        if len(file_name) < 1 or len(file_content_type) < 1 or len(
                file_md5) < 6 or len(file_path) < 1:
            if len(file_path) > 1:
                os.remove(file_path)
            self.write({
                "state": state.WEB_FAIL_PARAMS[0],
                "msg": state.WEB_FAIL_PARAMS[1],
                "result": {}
            })
            return
        #判断文件类型
        if not file_content_type or (
                file_content_type !=
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                and file_content_type != "application/octet-stream"):
            os.remove(file_path)
            self.write({
                "state": state.WEB_ERROR_FILE_FORMANT[0],
                "msg": state.WEB_ERROR_FILE_FORMANT[1],
                "result": {}
            })
            return
        calls_tuples = excel.read_excel_tuple(file_path)
        try:
            os.remove(file_path)
        except IOError as ex:
            app_log(ex)
        if calls_tuples:
            del calls_tuples[0]

            self.write({
                "state": state.WEB_SUCCESS[0],
                "msg": state.WEB_SUCCESS[1],
                "result": calls_tuples
            })
        else:
            self.write({
                "state": state.WEB_FAIL[0],
                "msg": state.WEB_FAIL[1],
                "result": {}
            })