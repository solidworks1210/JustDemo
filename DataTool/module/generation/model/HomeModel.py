# -*- coding:utf-8 -*-
# --------------------
# Author:       SDN
# Description:
# Time:         2017/3/1
# --------------------
import StringIO

from PIL import Image

from base_model import *

# 公司介绍
from utils import ImageUtils


def get_desc():
    """
    获取公司介绍内容
    :return:
    """
    content = msql.query("select content, id from item where category='description' limit 1")
    if len(content) == 1:  # 表中有内容
        if content[0]['content'] is None or content[0]['content'] == 'None':
            content[0]['content'] = ''
        return content[0]
    else:  # 表中没有内容，创建表内容
        return {'id': TimeUtils.time_id(), 'content': ""}


def save_descr(id_item, content):
    """
    保存公司介绍到数据库
    :param id_item:
    :param content:
    :return:
    """
    try:
        sql = "select id from item where id=%s"
        result = msql.query(sql, id_item)
        data_time = TimeUtils.datetime_date_simple()
        # 存在更新
        if len(result) != 0:
            result = msql.update('update item '
                                 'set content=%s, modified=%s where id=%s',
                                 content, data_time, id_item)
            msql.commit()
            return result
        # 不存在，插入
        else:
            result = msql.insert("insert into item "
                                 "(id, content, category, created, modified) "
                                 "values (%s, %s, %s, %s, %s)",
                                 id_item, content, 'description', data_time, data_time)
            msql.commit()
            return result
    except Exception as e:
        print 'HomeModel: ', e
        msql.rollback()
        return -1
