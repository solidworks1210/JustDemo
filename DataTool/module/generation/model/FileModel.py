# -*- coding:utf-8 -*- 
# --------------------
# Author:       SDN
# Description:
# Time:         2017/3/1
# --------------------
import StringIO

import re
from PIL import Image

from base_model import *


# 保存
from utils import ImageUtils


def save_file(file_save, table_file, category, id_user):
    """
    保存原始图片，返回路径
    :param file_save: 要保存的文件
    :param table_file: 文件保存的表
    :param category: 分类
    :param id_user: 使用者id
    :return:
    """
    try:
        # 获取文件后缀
        filename = file_save['filename']  # 只有上传文件对应的part才有该键，通过抛出异常来获得有效文件
        file_suffix = PathUtils.get_file_suffix(filename)
        # 文件类型
        file_type = file_save['content_type']  # u'image/jpeg'
        file_type_a = ''
        if '/' in file_type:
            file_type_a = file_type.split('/')[0]
        elif '\\' in file_type['type']:
            file_type_a = file_type['type'].split('\\')[0]
        elif '\\\\' in file_type['type']:
            file_type_a = file_type['type'].split('\\\\')[0]

        # # 数据库路径
        # path_origin_db, path_file_db, path_thumb_db = get_path_db(category=category, suffix=file_suffix)
        # # 文件保存路径
        # path_origin_save = os.path.join(path.PATH_STATIC, path_origin_db)
        # # 创建保存路径
        # path_folder_save = os.path.join(path.PATH_STATIC, make_folder_path())
        # if not os.path.exists(path_folder_save):
        #     os.makedirs(path_folder_save)

        # 生成文件名
        name_use = make_name_with_user_id(category=category, id_user=id_user, category_file='u', suffix=file_suffix)
        # 文件夹相对路径： files/upload/2017/3/24
        path_folder_relative_no_static = make_path_folder_relative_no_static()
        # 文件夹绝对对路径：..../static/files/upload/2017/3/24
        path_folder_absolute = PathUtils.connect(path.PATH_STATIC, path_folder_relative_no_static)
        # 文件保存绝对路径
        path_save_use = PathUtils.connect(path_folder_absolute, name_use)
        # 数据库路径
        path_db_use = PathUtils.to_url(PathUtils.connect(path_folder_relative_no_static, name_use))
        # 创建保存路径
        if not os.path.exists(path_folder_absolute):
            os.makedirs(path_folder_absolute)

        # 从字符串生成图片
        im = Image.open(StringIO.StringIO(file_save['body']))
        weight_image = len(file_save['body'])
        if weight_image > 100 * 1024:  # 富文本图片不能大于100kb
            ImageUtils.compress_image_file_by_width_limit(
                image_file=im,
                image_type=file_type,
                save_path=path_save_use,
                width_limit=1024,
                quality=65
            )
        else:
            print __name__, '富文本图片weight未超标，使用原图'
            im.save(path_save_use)
        size_origin = os.path.getsize(path_save_use)
        print __name__, '保存原图：', path_save_use
        id_origin = TimeUtils.time_id()
        date_time = TimeUtils.datetime_date_simple()
        param_origin = {
            'id': id_origin,
            'title': id_origin,
            'type': file_type,
            'type_a': file_type_a,
            'suffix': file_suffix,
            'created': date_time,
            'modified': date_time,
            'size': size_origin,
            'user': id_user,
            'category': category,
            'category_file': 'use',
            'path': path_db_use
        }
        insert_one_item(table_file, **param_origin)

        # 返回数据
        return add_static(path_db_use)
    except Exception as e:
        print __name__, '图片保存出错：', e
        return ''


def save_upload_file(poststreamer, id_user, title, category, table_file):
    """
    返回文件路径、文件 id
    :param table_file:
    :param category: 使用者所在分类
    :param title: 文件标题
    :param id_user: 使用者id
    :param poststreamer:
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
    for part in poststreamer.parts:
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
            file_args['suffix'] = PathUtils.get_file_suffix(filename)
            file_args['id'] = TimeUtils.time_id()
            file_args['user'] = id_user
            file_args['category'] = category
            file_args['category_file'] = 'attachment'
            file_args['created'] = TimeUtils.datetime_date_simple()
            file_args['size'] = part["size"]
            file_args['title'] = clean_file_name(title)
            if len(file_args['title']) == 0:
                file_args['title'] = str(file_args['id'])
            # 文件类型
            file_args['type'] = part["headers"][1].get("value", "text/plain")
            if '/' in file_args['type']:
                file_args['type_a'] = file_args['type'].split('/')[0]
            elif '\\' in file_args['type']:
                file_args['type_a'] = file_args['type'].split('\\')[0]
            elif '\\\\' in file_args['type']:
                file_args['type_a'] = file_args['type'].split('\\\\')[0]
            # 文件名：id_user file_title suffix
            name_file = StringUtils.connect(file_args['category'], '_', id_user, '-', file_args['id'], '-', file_args['title'], file_args['suffix'])
            path_folder_relative = make_path_folder_relative_no_static()
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
            # print e
            part["tmpfile"].close()
            os.unlink(part["tmpfile"].name)  # 删除临时文件（有多个，只有一个是上传文件）
    # 将信息写入数据库
    if len(file_info) > 0:
        result = insert_one_item(table_file, **file_info)
        if result != -1:
            return {
                'id_file': file_info['id'],
                'path_file': file_info['path'],
                'title_file': file_info['title']
            }
        else:
            return {}
    else:
        return {}

