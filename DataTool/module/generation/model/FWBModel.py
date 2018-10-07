# -*- coding:utf-8 -*- 
# --------------------
# Author:       SDN
# Description:
# Time:         2017/3/1
# --------------------

from tornado.escape import json_decode
from base_model import *
from utils import Thumbnail
from utils import utils


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


def get_one_item_by_id(id_item, table_item):
    """
    通过id从数据库获得条目的详情
    :param id_item:
    :param table_item:
    :return:
    """
    try:
        sql_get = StringUtils.connect("select * from ", table_item, " where id=%s")
        result = msql.get(sql_get, id_item)
        if result:
            result['created'] = TimeUtils.simplify_date(result['created'])
            result['modified'] = TimeUtils.simplify_date(result['modified'])
            result['attachments'] = get_attachment_dict_list(result['attachment_list'])
            try:
                if result['attachment_list']:  # None
                    json_decode(result['attachment_list'])
                else:
                    result['attachment_list'] = '[]'
            except:
                result['attachment_list'] = '[]'

            return result
        else:
            return {}
    except Exception as e:
        print __name__, 'get one item by id exception: ', e
        return {}


# --------------------------------------------- 清理附件
def string_to_list(sting_list):
    """
    将字符串化的list转为python list
    :param sting_list:
    :return:
    """
    try:
        if sting_list:  # None
            return json_decode(sting_list)
        else:
            return []
    except:
        return []


def get_attachment_dict_list(attachment_list_string):
    """
    传入的参数是前端传来的字符串化的数组，通过tornado的json_decode方法，转换为python的list
    :param attachment_list_string: '['path>name', 'path>name']'
    :return: {name: path, name: path}
    """
    try:
        if attachment_list_string:  # None
            ttemp = json_decode(attachment_list_string)
            attachment_path_db = {}
            for attachment in ttemp:
                temppp = attachment.split(u'>')
                if len(temppp) == 2:
                    attachment_path_db[temppp[0]] = temppp[1]
            return attachment_path_db
        else:
            return {}
    except Exception as e:
        print __name__, 'get_attachment_dict_list exception: ', e
        return {}


def clean_attachment(attachment_new, table_file, id_user):
    """

    :param attachment_new:'['path>name', 'path>name]'
    :param table_file:
    :param id_user:
    :return:
    """
    def get_attachment_path_db_list(attachment_string):
        attachment_path_db = []
        for attachment in string_to_list(attachment_string):
            attachment_path_db.append(attachment.split(u'>')[0])
        return attachment_path_db

    # 获取上传附件的清单
    attachment_new_path_db = get_attachment_path_db_list(attachment_new)
    # 通过id_user获取附件
    sql_all_id = StringUtils.connect("select path from ", table_file,
                                     " where user=%s and category_file='attachment'")
    result0 = msql.query(sql_all_id, id_user)
    path_all = []
    for item in result0:
        path_all.append(item['path'])

    for path_db in path_all:
        if path_db not in attachment_new_path_db:
            del_file_and_record_by_path_db(path_db=path_db, table_file=table_file)


# ----------------------------------------------- 清理富文本内容
def clean_fwb_content(id_user, category, table_file, content_page, create_thumb=True, thumb_with=400, thumb_height=200):
    """
    清理富文本中不要的内容，要创建缩略图
    :param create_thumb:
    :param thumb_height:
    :param thumb_with:
    :param table_file: 文件记录保存的表
    :param id_user: 使用者 id
    :param category: 使用者 分类，通过该分类可以获取表信息， 生成缩略图时缩略图分类
    :param content_page: 富文本内容（包含图片)
    :return: 缩略图路径
    """
    sql_all_id = StringUtils.connect("select path from ", table_file, " where user=%s and category_file!='attachment'")
    result0 = msql.query(sql_all_id, id_user)
    path_all = []
    for item in result0:
        path_all.append(item['path'])

    # 获取编辑内容中的所有图片路径（带静态文件夹名）
    path_list = utils.get_all_image_path_in_content(content_page)
    # 获取富文本内容中在使用文件的数据库保存路径
    path_in_use = []
    for item in path_list:
        item = item.split('/')[2:]
        path_in_use.append(PathUtils.to_url(PathUtils.connect(*item)))
    # 清理文件
    for item in path_all:
        if item not in path_in_use:
            del_file_and_record_by_path_db(path_db=item, table_file=table_file)

    # 找到content中第一幅图片的位置(作为缩略图)
    if create_thumb:
        if len(path_list) >= 1:
            # content中的图片路径包含静态文件夹：/static/files/.......
            path_thumb_db = create_thumbnail_from_url_path(
                path_url=path_list[0],
                thumb_width=thumb_with,
                thumb_height=thumb_height
            )
            id_thumb = TimeUtils.time_id()
            thumb_args = {
                'id': id_thumb,
                'path': path_thumb_db,
                'user': id_user,
                'created': TimeUtils.datetime_date_simple(),
                'category': category,
                'title': str(id_thumb),
                'category_file': 'thumb'
            }
            insert_one_item(table=table_file, **thumb_args)
        else:
            path_thumb_db = ''  # 不将默认缩略图路径写入数库

        # 返回缩略图路径
        return path_thumb_db
    else:
        return ''


def clean_fwb_content_add_discard(id_user, table_file):
    """
    添加富文本内容时放弃，通过使用者 id，删除所有相关文件及记录
    :param id_user:
    :param table_file:
    :return:
    """
    del_file_and_record_by_id_user(id_user=id_user, table_file=table_file)


def clean_fwb_content_edit_discard(id_user, table_file, content):
    """
    编辑富文本内容时放弃，不能删除原缩略图
    :param id_user:
    :param table_file:
    :param content:
    :return:
    """
    # 获取该条目所有对应文件在数据库中保存的路径
    sql_all_id = StringUtils.connect('select path from ', table_file,
                                     " where user=%s and category_file!='attachment' and category_file!='thumb'")
    result0 = msql.query(sql_all_id, id_user)
    path_all = []
    for item in result0:
        path_all.append(item['path'])

    # 获取编辑内容中的所有图片路径（带静态文件夹名）
    path_list = utils.get_all_image_path_in_content(content)
    # 获取富文本内容中在使用文件的数据库保存路径
    path_in_use = []
    for item in path_list:
        item = item.split('/')[2:]
        path_in_use.append(PathUtils.to_url(PathUtils.connect(*item)))
    # 清理文件
    for item in path_all:
        if item not in path_in_use:
            del_file_and_record_by_path_db(path_db=item, table_file=table_file)


def create_thumbnail_from_url_path(path_url, thumb_width=400, thumb_height=400):
    """
    /static/files/.......suffix，对应的文件生成缩略图
    :param thumb_height:
    :param thumb_width:
    :param table_file: 文件所在的表
    :param path_url:
    :return:
    """
    # path_url 包含静态文件夹
    if path_url.startswith('/'):
        path_names = path_url[1:].split('/')
    else:
        path_names = path_url.split('/')
    folder_no_static = path_names[1:-1]  # 文件夹（因原路径含静态文件夹，去除）
    name_houzui = path_names[-1]  # 文件名
    folder_path = ''
    for path_name in folder_no_static:
        folder_path = os.path.join(folder_path, path_name)
    no_static = folder_path[:]

    # print no_static

    path_temp = os.path.join(path.PATH_STATIC, folder_path)
    name, houzui = os.path.splitext(name_houzui)
    path_source = os.path.join(path_temp, name_houzui)
    path_thumb_save = os.path.join(path_temp, name + '_thumb' + houzui)

    # 数据库中路径不包含静态文件夹
    path_thumb_return = StringUtils.connect(name, '_thumb' + houzui)
    path_thumb_return = StringUtils.connect('/', path_thumb_return)
    path_thumb_return = StringUtils.connect(no_static, path_thumb_return)
    path_thumb_return = PathUtils.to_url(path_thumb_return)

    # 创建缩略图
    if os.path.exists(path_source):
        Thumbnail.thumb(
            path_source,
            path_thumb_save,
            thumb_width=thumb_width,
            thumb_height=thumb_height
        )
        print __name__, 'create thumb success: ', path_thumb_return
        return path_thumb_return
    else:
        return ''  # 源文件不存在，使用默认图片
