#!/usr/bin/env python
# -*- coding:utf-8 -*- 
# --------------------
# Author:       SDN
# Description:  加密
# --------------------
import hashlib


def check_pwd(pwd):
    """
    密码验证，在修改密码时验证密码的位数、字符范围
    :param pwd: 原始密码字符串
    :return:
    """
    # todo: check password
    return True


def md5(s):
    """
    基于hashlib的md5加密
    :param s: string or buffer
    :return:
    """
    m = hashlib.md5()
    m.update(s)
    return m.hexdigest()


if __name__ == '__main__':
    print len(md5('123456'))