# -*- coding:utf-8 -*- 
# --------------------
# Author:       SDN
# Description:	字符串操作相关
# Time:         2017/3/20
# --------------------


def connect(*args):
    """
    拼接字符串：不同编码的可以比较，但不能直接拼接
    :return:
    """
    if len(args) > 0:
        result = ''
        # 全转为字符串
        for item in args:
            if type(item) == type(u''):
                item = item.encode('utf-8')
            elif type(item) == type(1):
                item = str(item)
            elif type(item) == type(0.1):
                item = str(item)
            elif type(item) == type(3L):
                item = str(item)
            result += item
        return result
    else:
        return ''
