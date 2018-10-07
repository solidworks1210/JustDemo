# -*- coding:utf-8 -*- 
# --------------------
# Author:       SDN
# Description:	基本的Model，其它model继承，包含一些共用的方法
# --------------------
import re
import time

from config import config
from config import path
from utils import CodeUtils
from utils import PathUtils
from utils import StringUtils
from utils import TimeUtils
from utils.tornmq import Connection


class BaseModel(object):
    def __init__(self):
        self.db = Connection(
            user=config.USER, password=config.PASSWORD,
            port=config.PORT, host=config.HOST, database=config.DATABASE
        )

    def get_total_pages(self, table, category, items_per_page):
        try:
            sql_total = StringUtils.connect("select count(*) from ", table, " where category=%s")
            all_items = self.db.row_count(sql_total, category)
            if all_items % items_per_page != 0:
                page_total = all_items / items_per_page + 1
            else:
                page_total = all_items / items_per_page
            return page_total
        except Exception as e:
            print __name__, 'total_pages except: ', e
            return 0

    @staticmethod
    def add_static(path_db):
        """
        将数据库中保存的地址转为网站资源地址
        'file/.....' to '/static/file/.......
        """
        return PathUtils.to_url(StringUtils.connect('/', path.NAME_STATIC, '/', path_db))

    def insert_one_item(self, table, **kwargs):
        """
        插入一条到数据库（先判断 id 是否存在，存在为更新，不在为插入）
        :param table: 要保存的表
        :param kwargs:
        :return:
        """
        if len(kwargs) > 0:
            # 插入前先判断是否存在（保证 id 唯一）
            try:
                # 是否存在
                sql_query = StringUtils.connect('select id from ', table, ' where id=%s')
                result_temp = self.db.get(sql_query, kwargs['id'])
                # 已存在，更新
                if result_temp:
                    id_update = kwargs.pop('id')  # 更新前剔除 id
                    print __name__, '存在更新：', table
                    return self.db.update_one(table, id_update, **kwargs)
                # 不存在，插入
                else:
                    return self.db.insert_one(table, **kwargs)
            except Exception as e:
                print __name__, '判断是否存在出错:', e
                return -1
        else:
            return -1

    # ——————————————生成路径

    @staticmethod
    def make_name_with_user_id(category, id_user, category_file, suffix):
        """
        文件名字
        category_id_user TimeUtils.data_name_full().suffix
        生成文件名字, 如果给定的名字包含 unicode，转为 str
        :param category_file: o 原图，u 使用图，t 缩略图
        :param category: 文件分类
        :param suffix: 文件后缀
        :param id_user:  使用者id
        :return:
        """
        name_file = StringUtils.connect(category, '_', id_user, ' ',
                                        TimeUtils.datetime_name_full(), '_',
                                        category_file, suffix)
        return name_file

    @staticmethod
    def make_path_folder_relative_no_static():
        """
        文件夹相对路径
        :return: files\upload\2017\3\24\
        """
        now_date = time.localtime()
        now_year = str(now_date[0])
        now_month = str(now_date[1])
        now_day = str(now_date[2])
        return PathUtils.connect(path.PATH_UPLOAD, now_year, now_month, now_day)

    @staticmethod
    def remove_static(path_url, use_unicode=False):
        """
        移除url中的静态文件夹：/static/files/..... to files/.......
        :param use_unicode: True: 返回unicode， False 返回str
        :param path_url:
        :return:
        """
        if isinstance(path_url, type(u'')):
            result = u'/'.join(path_url.split(u'/')[2:])
            if use_unicode:
                return result
            else:
                return result.encode('utf-8')
        elif isinstance(path_url, type('')):
            result = '/'.join(path_url.split('/')[2:])
            if use_unicode:
                return result.decode('utf-8')
            else:
                return result

    # ———————————————————— 移除富文本内容中图片的 height 属性
    @staticmethod
    def remove_image_height_attr(content):
        """
        移除富文本图片的height属性
        :param content:
        :return:
        """
        content = CodeUtils.to_str(content)
        image_tags = re.findall(r'<img.*?>', content)
        for tag in image_tags:
            tag_temp = re.sub(r'height.*?;', '', tag)
            # content = re.sub(tag, tag_temp, content)  # 中文带括号时不能替换
            content = content.replace(tag, tag_temp)
        return content
