# -*- coding:utf-8 -*- 
# --------------------
# Author:       SDN
# Description:	视频、图片、文件处理类
# Time:         2017/3/6
# --------------------
import os

import tornado.web
from tornado.escape import json_encode

from BaseHandler import BaseHandler
from config import path
from module.generation.model import FileModel
from module.generation.utils import post_streamer

# 富文本图片上传
class ImageHandler(BaseHandler):
    """
    图片接收，用于小文件
    """

    @tornado.web.authenticated
    def post(self):
        # var params = {
        #     '_xsrf': getCookie('_xsrf'),
        #     'id_user': {{id_item}},
        #     'category': {{role_page}}
        # }
        category = self.get_argument('category', strip=True)  # 分类
        id_user = self.get_argument('id_user', strip=True)  # 使用者 id
        if len(category) != 0 and len(id_user) != 0:
            try:
                file_save = self.request.files['photo'][0]
                # 保存文件
                result_temp = FileModel.save_file(
                    file_save=file_save,
                    table_file='file',
                    category=category,
                    id_user=id_user
                )
                if len(result_temp) > 0:
                    self.write(result_temp)
                else:
                    print __name__, '文件保存失败'
                    self.write('false')
            except Exception, e:
                print __name__, '未选择文件：', e
                self.write('false')
        else:
            print __name__, '文件参数不存在'
            self.write('false')

# 以下为大文件上传
class MyPostDataStreamer(post_streamer.PostDataStreamer):
    percent = 0

    # def on_progress(self): #这个方法显示实时进度，直接在前端就可以实现，因此暂时不需要这方法了
    def xx__on_progress(self):  # 改成其它名字，也不影响程序运行
        """Override this function to handle progress of receiving data."""
        if self.total:
            new_percent = self.received * 100 // self.total
            if new_percent != self.percent:
                self.percent = new_percent
                print("progress", new_percent)


@tornado.web.stream_request_body
class FileUploadAjaxHandler(tornado.web.RequestHandler):
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
        self.ps = MyPostDataStreamer(total, tmpdir=path.PATH_TEMP)  # 路径为临时文件保存路径（绝对路径）

    def data_received(self, chunk):
        """这个方法是tornado.web模块 stream_request_body 必须实现的数据接收方法"""
        self.ps.receive(chunk)

    def post(self):
        """
        前端不传除文件外的其他参数：文件名为当前时间的毫秒数、保存在分类（category）中的default文件夹
        :return:
        """
        # 必须显式调用ps的数据接收处理方法 finish_receive()
        self.ps.finish_receive()
        self.set_header("Content-Type", "text/plain")
        # 获取所有上传的参数
        all_upload_params = self.ps.get_values(self.ps.get_nonfile_names())
        # 转存文件，并将文件信息写入数据库(返回文件保存数据库路径、id)
        result = FileModel.save_upload_file(
            self.ps,
            id_user=all_upload_params['user'].strip(),
            title=all_upload_params['title'].strip(),
            category=all_upload_params['category'].strip(),
            table_file='file'
        )

        # 返回文件id，保存路径
        if len(result) > 0:
            # 'id_file': file_info['id'],
            # 'path_file': file_info['path']
            self.write(json_encode(result))
        else:
            self.write('')
