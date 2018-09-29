#!/usr/bin/env python
# -*- coding:utf-8 -*- 
# --------------------
# Author:       SDN
# Description:  工具类
# --------------------


def dict_revert(old_dict):
    """
    将字典的键值换位
    :param old_dict:
    :return:
    """
    return {value: key for key, value in old_dict.iteritems()}
