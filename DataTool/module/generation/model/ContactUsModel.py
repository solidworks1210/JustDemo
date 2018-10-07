# -*- coding:utf-8 -*- 
# --------------------
# Author:       SDN
# Description:
# Time:         2017/3/1
# --------------------

from base_model import *


def get_comment(page, items):
    """
    :param page: 当前显示的页数
    :param items: 每页显示多少条
    :return:
    """
    try:
        total = get_comment_total_pages(items)     # 总页数
        page_int = int(page) - 1
        if page_int == -1:
            page_int = 1
        offset = items*page_int
        items = msql.query('select * from comment order by created desc, name asc limit %s offset %s', items, offset)
        return total, items
    except Exception as e:
        print __name__, 'get_comment exception: ', e
        return 0, []


def get_comment_total_pages(items=10):
    """

    :param items: 每页显示多少条
    :return:
    """
    try:
        all_items = msql.row_count("select count(*) from comment")
        if all_items % items != 0:
            page_total = all_items / items + 1
        else:
            page_total = all_items / items
        return page_total
    except Exception as e:
        print __name__, 'total_pages except: ', e
        return 0


def get_one_comment(comment_id):
    result = msql.get("select * from comment where id=%s ", comment_id)
    return result


def delete_one_comment(del_id):
    try:
        result = msql.execute_rowcount("delete from comment where id=%s", del_id)
        msql.commit()
        return result
    except:
        msql.rollback()
        return 0
