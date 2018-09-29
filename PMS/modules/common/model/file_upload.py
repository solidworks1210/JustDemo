# -*- coding:utf-8 -*- 
# --------------------
# Author:       SDN
# Description:
# --------------------
import StringIO

import os
import traceback

import re
from PIL import Image
from tornado.log import app_log

from config import path
from module.manage.model.BaseModel import BaseModel
from utils import ImageUtils, PathUtils, TimeUtils, StringUtils


class FWBImageReceiveModel(BaseModel):
    """
    富文本编辑器，图片上传
    """

    def save_image(self, user_id, user_category, file_save):
        """
        保存富文本编辑器上传的图片: 图片要压缩, 图片转为jpeg格式
        :param user_id: 图片使用者的id
        :param user_category: 图片使用者的分类信息，通过分类信息dict，可以获取很多有用信息
        :param file_save: 要保存的文件
        :return: 图片保存的路径（含静态路径）
        """
        try:
            # 获取文件
            filename = os.path.splitext(file_save['filename'])[0]  # 只有上传文件对应的part才有该键，通过抛出异常来获得有效文件
            # 文件类型
            file_type_full = file_save['content_type']  # u'image/jpeg'
            if '/' in file_type_full:  # image
                file_type = file_type_full.split('/')[0]
            elif '\\' in file_type_full['type']:
                file_type = file_type_full['type'].split('\\')[0]
            elif '\\\\' in file_type_full['type']:
                file_type = file_type_full['type'].split('\\\\')[0]
            else:
                file_type = 'unknown'

            # 生成文件名
            name_use = self.make_file_name_with_user_id(
                user_category=user_category['category'],
                user_id=user_id,
                file_category='u',
                file_suffix='.jpg'
            )
            # 文件夹相对路径： files/upload/2017/3/24
            path_folder_relative_no_static = self.make_path_folder_relative_no_static()
            # 文件夹绝对对路径：..../static/files/upload/2017/3/24
            path_folder_absolute = PathUtils.connect(path.PATH_STATIC, path_folder_relative_no_static)
            # 文件保存绝对路径
            path_save_use = PathUtils.connect(path_folder_absolute, name_use)
            # 数据库路径
            path_db_use = PathUtils.to_url(PathUtils.connect(path_folder_relative_no_static, name_use))
            # 创建保存路径
            if not os.path.exists(path_folder_absolute):
                os.makedirs(path_folder_absolute)

            # 从字符串生成图片, 并保存为jpg（保存路径后缀决定）
            Image.open(StringIO.StringIO(file_save['body'])).save(path_save_use, format='jpeg')
            # 如果原始文件大小超标，压缩
            if os.path.getsize(path_save_use) > user_category['image_size_limit']:
                self.compress_image(image_file_path=path_save_use, category_info=user_category)
            file_size = os.path.getsize(path_save_use)
            image_id = TimeUtils.time_id()
            date_time = TimeUtils.datetime_date_simple()
            param_origin = {
                'id': image_id,
                'user_id': user_id,
                'user_category': user_category['category'],
                'file_category': 'use',
                'title': name_use,
                'summary': filename,
                'type': file_type,
                'created': date_time,
                'size': file_size,
                'path': path_db_use
            }
            self.insert_one_item(user_category['file_table'], **param_origin)

            # 返回数据
            return self.add_static(path_db_use)
        except Exception as e:
            traceback.print_exc()
            app_log.error(e)
            return ''


fwb_image_receive_model = FWBImageReceiveModel()


class FileReceiveModel(BaseModel):
    """
    大文件接收
    """

    def save_upload_file(self, post_streamer, user_id, user_category_info, file_title):
        """
        返回文件路径、文件 id
        :param post_streamer:
        :param user_id: 文件使用者id
        :param user_category_info: 文件使用者的分类
        :param file_title: 文件名称
        :return:
        """

        def clean_file_name(file_name):
            """
            去除文件名中不规范的项目(利用正则表达式)
            """
            re_str = r"[\/\\\:\*\?\"\<\>\| _]"  # '/\:*?"<>|'
            return re.sub(re_str, "", file_name)

        # 获取文件信息
        file_info = {}
        for part in post_streamer.parts:
            """
            [
                { headers:[ {params, name, value}, {params, name, value} ], tempile, size },    # part

                { headers:[ {params, name, value}, ], tempile, size },  # part
                { headers:[ {params, name, value}, ], tempile, size },  # part
                { headers:[ {params, name, value}, ], tempile, size },  # part
                { headers:[ {params, name, value}, ], tempile, size },  # part
                { headers:[ {params, name, value}, ], tempile, size },  # part
            ]
            0、poststreamer.parts，为一个 list 对象，其总共有六个 dict（headers、tempfile、size） 元素
            1、size 文件大小
            2、tempfile 值是一个临时文件对象 （转存要用到）
            4、headers 值是一个 list [ {params, name, value}, ]
            5、六个 dict 中，第一个为需要的

            """
            try:
                file_args = {}
                part["tmpfile"].close()
                # 获取文件后缀
                params = part["headers"][0].get("params", None)
                filename = params['filename']  # 只有上传文件对应的part才有该键，通过抛出异常来获得有效文件
                fill_suffix = PathUtils.get_file_suffix(filename)
                file_args['id'] = TimeUtils.time_id()
                file_args['user_id'] = user_id
                file_args['user_category'] = user_category_info['category']
                file_args['file_category'] = 'attachment'
                file_args['created'] = TimeUtils.datetime_date_simple()
                file_args['size'] = part["size"]
                file_args['title'] = clean_file_name(file_title)
                if len(file_args['title']) == 0:
                    file_args['title'] = str(file_args['id'])
                # 文件类型
                full_file_type = part["headers"][1].get("value", "text/plain")
                if '/' in full_file_type:
                    file_args['type'] = full_file_type.split('/')[0]
                elif '\\' in full_file_type:
                    file_args['type'] = full_file_type.split('\\')[0]
                elif '\\\\' in full_file_type:
                    file_args['type'] = full_file_type.split('\\\\')[0]
                # 文件名：id_user file_title suffix
                name_file = StringUtils.connect(file_args['user_category'], '_', file_args['user_id'], '-', file_args['id'], '-', file_args['title'], fill_suffix)
                path_folder_relative = self.make_path_folder_relative_no_static()
                path_folder_absolute = PathUtils.connect(path.PATH_STATIC, path_folder_relative)
                file_args['path'] = PathUtils.to_url(PathUtils.connect(path_folder_relative, name_file))
                path_save = PathUtils.connect(path_folder_absolute, name_file)
                if isinstance(path_save, type('')):
                    path_save = path_save.decode('utf-8')
                # 创建文件夹路径
                if not os.path.exists(path_folder_absolute):
                    os.makedirs(path_folder_absolute)
                # 转存文件（这步将临时文件保存为正式文件， 关键）
                os.rename(part["tmpfile"].name, path_save)
                if not os.path.exists(path_save):  # 判断是否转存成功
                    file_info = {}
                    continue
                file_info = file_args
                # break # 不能终止循环，要通过异常，来删除临时文件
            except Exception as e:
                # traceback.print_exc()
                part["tmpfile"].close()
                os.unlink(part["tmpfile"].name)  # 删除临时文件（有多个，只有一个是上传文件）
        # 将信息写入数据库
        if len(file_info) > 0:
            result = self.insert_one_item(user_category_info['file_table'], **file_info)
            if result != -1:
                return {
                    '': file_info['id'],
                    'file_path': file_info['path'],
                    'file_title': file_info['title']
                }
            else:
                return {}
        else:
            return {}


file_receive_model = FileReceiveModel()
