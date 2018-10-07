# -*- coding:utf-8 -*- 
# --------------------
# Author:       SDN
# Description:	编码相关的方法
# Time:         2017/4/15
# --------------------

def to_unicode(content):
    """
    将给定字符串转为unicode, None to u''
    :param content:
    :return:
    """
    if content:
        if isinstance(content, type('')):
            return content.decode('utf-8')
        elif isinstance(content, type(u'')):
            return content
        else:
            raise '不是字符串'
    else:
        return u''


def to_str(content):
    """
        将给定字符串转为str, None to ''
        :param content:
        :return:
        """
    if content:
        if isinstance(content, type(u'')):
            return content.encode('utf-8')
        elif isinstance(content, type('')):
            return content
        else:
            raise '不是字符串'
    else:
        return ''