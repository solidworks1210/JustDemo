#!/usr/bin/env python
# -*- coding:utf-8 -*- 
# --------------------
# Author:       SDN
# Description:  文件保存model
# --------------------

import os
from tornado.httputil import HTTPFile

from modules.common.model.base import BaseModel

from tornado.log import app_log


class ShareModel(BaseModel):
    def save_form_file(self, file_data, user_info):
        """保存通过form表单提交的文件"""

        file_name, suffix = os.path.splitext(file_data['filename'])
        file_body = file_data['body']

        file_path = None