# -*- coding:utf-8 -*- 
# --------------------
# Author:       SDN
# Description:
# Time:         2017/3/1
# --------------------
import StringIO

from PIL import Image

from base_model import *
from utils import ImageUtils
from utils import Thumbnail


def get_item_list(table, category, page_current, items):
    """
    获取条目清单
    :param table:
    :param category: 条目所在分类
    :param page_current: 当前页数
    :param items: 每页条数
    :return:
    """
    try:
        if page_current == 0:
            page_current = 1
        offset = items * (page_current - 1)
        sql_query = StringUtils.connect("select * from ", table,
                                        " where category=%s order by created desc, title asc limit %s offset %s")
        item_list = msql.query(sql_query, category, items, offset)
        for item in item_list:
            item['created'] = TimeUtils.simplify_date(item['created'])
            item['modified'] = TimeUtils.simplify_date(item['modified'])
            item['path_thumb'] = add_static(item['path_thumb'])
            item['path_file'] = add_static(item['path_file'])
        return total_pages(table, category, items), item_list
    except Exception as e:
        print __name__, 'get_item_list except: ', e
        return 0, []


def total_pages(table, category, items=10):
    """
    获取该分类总页数
    :param table:
    :param category:
    :param items:
    :return:
    """
    try:
        sql_total = StringUtils.connect("select count(*) from ", table, " where category=%s")
        all_items = msql.row_count(sql_total, category)
        if all_items % items != 0:
            page_total = all_items / items + 1
        else:
            page_total = all_items / items
        return page_total
    except Exception as e:
        print __name__, 'total_pages except: ', e
        return 0


def save_selector(file_save, table_file, category, id_user,
                  size_limit, quality_limit, width_limit, height_limit, width_thumb, height_thumb, compress_type=0):
    """

    :param file_save:
    :param table_file:
    :param category:
    :param id_user:
    :param size_limit:
    :param quality_limit:
    :param width_limit:
    :param height_limit:
    :param width_thumb:
    :param height_thumb:
    :param compress_type: 1: 按宽限制等比例压缩，2 按宽高限制压缩， 3 按高压缩, 4 调整到给定宽高
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
        # path_file_save = os.path.join(path.PATH_STATIC, path_file_db)
        # path_thumb_save = os.path.join(path.PATH_STATIC, path_thumb_db)
        # # 创建保存路径
        # path_folder_save = os.path.join(path.PATH_STATIC, make_folder_path())
        # if not os.path.exists(path_folder_save):
        #     os.makedirs(path_folder_save)


        # 生成文件名
        name_origin = make_name_with_user_id(category=category, id_user=id_user, category_file='o', suffix=file_suffix)
        name_use = make_name_with_user_id(category=category, id_user=id_user, category_file='u', suffix=file_suffix)
        name_thumb = make_name_with_user_id(category=category, id_user=id_user, category_file='t', suffix=file_suffix)
        # 文件夹相对路径： files/upload/2017/3/24
        path_folder_relative_no_static = make_path_folder_relative_no_static()
        # 文件夹绝对对路径：..../static/files/upload/2017/3/24
        path_folder_absolute = PathUtils.connect(path.PATH_STATIC, path_folder_relative_no_static)
        # 文件保存绝对路径
        path_save_origin = PathUtils.connect(path_folder_absolute, name_origin)
        path_save_use = PathUtils.connect(path_folder_absolute, name_use)
        path_save_thumb = PathUtils.connect(path_folder_absolute, name_thumb)
        # 数据库路径
        path_db_origin = PathUtils.to_url(PathUtils.connect(path_folder_relative_no_static, name_origin))
        path_db_use = PathUtils.to_url(PathUtils.connect(path_folder_relative_no_static, name_use))
        path_db_thumb = PathUtils.to_url(PathUtils.connect(path_folder_relative_no_static, name_thumb))
        # 创建保存路径
        if not os.path.exists(path_folder_absolute):
            os.makedirs(path_folder_absolute)

        # 从字符串生成图片
        im = Image.open(StringIO.StringIO(file_save['body']))
        # 保存原图
        im.save(path_save_origin)
        size_origin = os.path.getsize(path_save_origin)
        print __name__, '保存原图：', path_save_origin
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
            'category_file': 'origin',
            'path': path_db_origin
        }
        insert_one_item(table_file, **param_origin)
        # 保存使用图(不管图片的weight， 按压缩方式压缩)
        if compress_type == 1:  # 按宽压缩，对于jpg添加质量保存（最终宽在限内，高不一定）
            ImageUtils.compress_image_file_by_width_limit(
                image_file=im,
                image_type=file_type,
                save_path=path_save_use,
                width_limit=width_limit,
                quality=quality_limit
            )
        elif compress_type == 3:    # 按高压缩，对于jpg添加质量保存（最终高在限内，宽不一定）
            ImageUtils.compress_image_file_by_height_limit(
                image_file=im,
                image_type=file_type,
                save_path=path_save_use,
                height_limit=height_limit,
                quality=quality_limit
            )
        elif compress_type == 4:    # 把图片缩放到给定的尺寸
            ImageUtils.fit_dimension_from_image_file(
                image_file=im,
                image_type=file_type,
                save_path=path_save_use,
                width_limit=width_limit,
                height_limit=height_limit,
                quality=quality_limit
            )
        else:   # 按宽高压缩，对于jpg添加质量保存（最终尺寸在宽高限内）
            ImageUtils.compress_image_file_by_dimension_limit(
                image_file=im,
                image_type=file_type,
                save_path=path_save_use,
                width_limit=width_limit,
                height_limit=height_limit,
                quality=quality_limit
            )
        size_file = os.path.getsize(path_save_use)
        print __name__, '保存用图：', path_save_use
        id_file = TimeUtils.time_id() + 2
        param_file = {
            'id': id_file,
            'title': id_file,
            'type': file_type,
            'type_a': file_type_a,
            'suffix': file_suffix,
            'created': date_time,
            'modified': date_time,
            'size': size_file,
            'user': id_user,
            'category': category,
            'category_file': 'use',
            'path': path_db_use
        }
        insert_one_item(table_file, **param_file)
        # 保存缩略图
        Thumbnail.thumb2(imgFile=im, outputDir=path_save_thumb, thumb_width=width_thumb, thumb_height=height_thumb)
        size_thumb = os.path.getsize(path_save_thumb)
        print __name__, '保存缩图：', path_save_thumb
        id_thumb = TimeUtils.time_id() + 4
        param_thumb = {
            'id': id_thumb,
            'title': id_thumb,
            'type': file_type,
            'type_a': file_type_a,
            'suffix': file_suffix,
            'created': date_time,
            'modified': date_time,
            'size': size_thumb,
            'user': id_user,
            'category': category,
            'category_file': 'thumb',
            'path': path_db_thumb
        }
        insert_one_item(table_file, **param_thumb)
        # 返回数据
        return {
            'path_origin': path_db_origin,
            'path_file': path_db_use,
            'path_thumb': path_db_thumb
        }
    except Exception as e:
        print __name__, '图片保存出错：', e
        return {}


def change_selector(file_save, table_file, category, id_user,
                    size_limit, quality_limit, width_limit, height_limit, width_thumb, height_thumb, compress_type=0):

    # 根据使用者id删除文件
    del_file_and_record_by_id_user(id_user=id_user, table_file=table_file)
    # 保存新图
    return save_selector(file_save, table_file, category, id_user,
                         size_limit, quality_limit, width_limit, height_limit, width_thumb, height_thumb, compress_type)


def delete_one_item_by_id(id_del, table_item, table_file):
    """
    通过条目id，删除条目，以及文件和记录
    :param id_del:
    :param table_item:
    :param table_file:
    :return:
    """
    try:
        # 删除文件、记录
        del_file_and_record_by_id_user(id_user=id_del, table_file=table_file)
        # 删除该条目数据库记录
        slq_del = 'delete from ' + table_item + ' where id=%s'
        result = msql.execute_rowcount(slq_del, id_del)
        msql.commit()
        print __name__, 'delete_one_item_by_id: ', result
        return result
    except Exception as e:
        print __name__, 'delete_one_item_by_id exception: ', e
        msql.rollback()
        return -1
