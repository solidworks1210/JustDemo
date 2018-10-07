# -*- coding:utf-8 -*- 
# --------------------
# Author:       SDN
# Description:	输入验证
# Time:         2017/3/18
# --------------------


def verify_name(name_input):
    """

    :param name_input: 用户输入
    :return:
    """
    if len(name_input) != 0:
        return True
    else:
        return False


def verify_ps(ps_input):
    """
    :param ps_input: 用户输入的密码
    :return:
    """
    if len(ps_input) >= 6:
        result = True
    else:
        result = False
    return result
