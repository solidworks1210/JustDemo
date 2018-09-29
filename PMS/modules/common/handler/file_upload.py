# -*- coding:utf-8 -*- 
# --------------------
# Author:       SDN
# Description:	视频、图片、文件处理类
# --------------------
import os
import traceback

import tornado.gen
import tornado.web
import tornado.concurrent
from tornado.escape import json_encode
from tornado.log import app_log

from modules.common.handler.base import BaseHandler


# 富文本图片接收
from modules.common.model.file_upload import fwb_image_receive_model


class FWBImageReceiveHandler(BaseHandler):
    """
    用于接收富文本编辑器添加的图片, 返回的图片保存路径(含静态路径），出错返回默认图片的路径
    """

    @tornado.web.authenticated
    @tornado.gen.coroutine
    def post(self):
        result = yield self.action()
        self.write(result)

    @tornado.concurrent.run_on_executor(executor='thread_pool')
    def action(self):
        user_id = self.get_argument('user_id', strip=True)  # 使用者 id
        category = self.get_argument('user_category', strip=True)  # 分类
        if category and user_id:
            try:
                file_save = self.request.files['photo'][0]
                # 保存文件
                result_temp = fwb_image_receive_model.save_image(
                    user_id=user_id,
                    user_category=self.get_category_info(category),
                    file_save=file_save,
                )
                if len(result_temp) > 0:
                    return result_temp
                else:
                    return DEFAULT_IMAGE_PATH
            except Exception, e:
                traceback.print_exc()
                app_log.error(e)
                return DEFAULT_IMAGE_PATH
        else:
            return DEFAULT_IMAGE_PATH


# 文件上传接收（支持大文件）
@tornado.web.stream_request_body
class FileReceiveHandler(BaseHandler):
    """
    前端传来的参数：
    1、title：自定义的文件名，不能为空（重命名文件用）
    2、id：文件的 id 号， 毫秒时间（作为数据库 id）
    3、category：文件分类（）
    4、description: 文件描述（可以为空）
    5、user: 使用者的id（可为空）

    a、一个文件分类就是一个表，分类名就是表名。
    b、一个文件分类就是一个文件夹，分类名就是文件夹名，在分类文件夹中按时间建立层级文件夹
    c、表中保存的路径是url格式的，不包含静态文件夹
    d、文件名是自己取的名字和添加时间的组合2017.... 文件名（文件名中要把空格去除，以 . 替代）
    """

    def prepare(self):
        """定义一个PostDataStreamer，作为stream_request_body接收data的处理类"""
        try:
            total = int(self.request.headers.get("Content-Length", "0"))
        except:
            total = 0
        if not os.path.exists(path.PATH_TEMP):
            os.makedirs(path.PATH_TEMP)
        self.post_streamer = post_streamer.PostDataStreamer(total, tmpdir=path.PATH_TEMP)  # 路径为临时文件保存路径（绝对路径）

    def data_received(self, chunk):
        """这个方法是tornado.web模块 stream_request_body 必须实现的数据接收方法"""
        self.post_streamer.receive(chunk)

    def post(self):
        """
        前端不传除文件外的其他参数：文件名为当前时间的毫秒数、保存在分类（category）中的default文件夹
        :return:
        """
        # 必须显式调用post_streamer.PostDataStreamer的数据接收处理方法 finish_receive()
        self.post_streamer.finish_receive()
        self.set_header("Content-Type", "text/plain")
        # 获取所有上传的参数
        all_upload_params = self.post_streamer.get_values(self.post_streamer.get_nonfile_names())
        # 转存文件，并将文件信息写入数据库(返回文件保存数据库路径、id)
        result = file_receive_model.save_upload_file(
            self.post_streamer,
            user_id=all_upload_params['user_id'].strip(),
            user_category_info=self.get_category_info(all_upload_params['user_category'].strip()),
            file_title=all_upload_params['file_title'].strip(),
        )

        # 返回文件id，保存路径
        if result:
            self.write({'status': 1, 'msg': 'success', 'data': result})
        else:
            self.write({'status': 0, 'msg': 'false'})
