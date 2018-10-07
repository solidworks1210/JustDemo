# -*- coding:utf-8 -*-
# --------------------
# Author:       SDN
# Description:
# Time:         2017/3/1
# --------------------
import threading

from PIL import Image

from base_model import *
from utils import ImageUtils
from utils import utils


def get(role):
    """
    根据角色获得其对应的内容
    :return:
    """
    try:
        content = msql.query("select * from item where category=%s order by created asc limit 1", role)
        if len(content) == 1:   # 存在
            return content[0]
        else:   # 不存在, 创建
            return {'id': TimeUtils.time_id(), 'content': ''}
    except Exception as e:
        print __name__, '获取信息出错: ', e
        return {'id': TimeUtils.time_id(), 'content': ''}


def save(**kwargs):
    """
    保存
    :param kwargs:
    :return:
    """
    return insert_one_item('item', **kwargs)
