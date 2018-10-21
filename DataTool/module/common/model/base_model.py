# -*- coding:utf-8 -*- 
# --------------------
# Description:	基本的Model，其它model继承，包含一些共用的方法
# --------------------

from config import config
from utils import StringUtils
from utils.tornsq import Connection

db_connect = Connection(config.DB_PATH)


class BaseModel(object):
    """
    数据库公用一个连接
    """

    def __init__(self, same_connect=True):
        """

        :param same_connect: True 使用同一个连接；False 新建连接
        """
        if same_connect is True:
            self.db = db_connect
        else:
            self.db = Connection(config.DB_PATH)

    def get_total_pages(self, table, category, items_per_page):
        """

        :param table:
        :param category:
        :param items_per_page:
        :return:
        """
        try:
            sql_total = StringUtils.connect("select count(*) from ", table, " where category=%s")
            all_items = self.db.count(sql_total, category)
            if all_items % items_per_page != 0:
                page_total = all_items / items_per_page + 1
            else:
                page_total = all_items / items_per_page
            return page_total
        except Exception as e:
            print __name__, 'total_pages except: ', e
            return 0
