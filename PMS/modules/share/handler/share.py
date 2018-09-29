#!/usr/bin/env python
# -*- coding:utf-8 -*-
# --------------------
# Author:       SDN
# Description:  文件共享
# --------------------
import base64
import os
import os.path

import tornado.web
from tornado import gen
from tornado import iostream

from configs.config import STATIC_PATH
from modules.common.handler.base import BaseHandler

file_upload_path = os.path.join(STATIC_PATH, 'upload')


class IndexHandler(BaseHandler):
    @tornado.web.asynchronous
    def get(self):
        self.render_params['title'] = '分享管理'
        self.render_params['flags'] = self.get_flags(__name__)
        items = []
        for filename in os.listdir(file_upload_path):
            print type(filename), filename.encode('utf-8')
            items.append(filename)
        self.render_params['items'] = items
        self.render('share.html', render_params=self.render_params)

    def post(self):
        """上传"""
        file_data = self.request.files['file'][0]

        file_content = self.request.files['file'][0]['body']
        file_name = self.request.files['file'][0]['filename']
        pat = os.path.join(file_upload_path, file_name)
        x = open(pat, 'wb')
        x.write(file_content)
        x.close()
        self.redirect("/share")


class DownloadHandler0(BaseHandler):
    """下载"""

    @tornado.web.asynchronous
    def get(self):
        file_path = os.path.join(file_upload_path, '123.mkv')

        # http头 浏览器自动识别为文件下载
        self.set_header('Content-Type', 'application/octet-stream')
        # self.set_header('Content-Type', 'text/csv')
        # 下载时显示的文件名称
        self.set_header('Content-Disposition', 'attachment; filename=%s' % '123.mkv')
        with open(file_path, 'rb') as f:
            while True:
                data = f.read(1024)
                if not data:
                    break
                self.write(data)
        # # 记得有finish哦
        self.finish()


class DownloadHandler(BaseHandler):
    """异步下载文件"""
    @gen.coroutine
    def get(self):
        file_path = os.path.join(file_upload_path, '123.mkv')
        content_length = os.path.getsize(file_path)
        self.set_header("Content-Length", content_length)
        self.set_header("Content-Type", "application/octet-stream")
        self.set_header("Content-Disposition", "attachment;filename=\"{0}\"".format("123.mkv"))  # 设置新的文件名
        content = self.get_content(file_path)
        if isinstance(content, bytes):
            content = [content]
        for chunk in content:
            try:
                self.write(chunk)
                yield self.flush()
            except iostream.StreamClosedError:
                break
        return

    # 使用python自带的对于yield的应用对文件进行切片，for循环每运用一次就调用一次
    def get_content(self, file_path):
        start = None
        end = None
        with open(file_path, "rb") as file0:
            if start is not None:
                file0.seek(start)
            if end is not None:
                remaining = end - (start or 0)
            else:
                remaining = None
            while True:
                chunk_size = 64 * 1024  # 每片的大小是64K
                if remaining is not None and remaining < chunk_size:
                    chunk_size = remaining
                chunk = file0.read(chunk_size)
                if chunk:
                    if remaining is not None:
                        remaining -= len(chunk)
                    yield chunk
                else:
                    if remaining is not None:
                        assert remaining == 0
                    return


class ParserFilename(tornado.web.StaticFileHandler):
    def data_received(self, chunk):
        pass

    def initialize(self, path):
        # print 'the path is',path
        # self.dirname, self.filename = os.path.split(path)
        super(ParserFilename, self).initialize(path)

    def parse_url_path(self, url_path):
        url_path = base64.b64decode(url_path)
        if os.path.sep != "/":
            url_path = url_path.replace("/", os.path.sep)
        return url_path