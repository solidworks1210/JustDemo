# -*- coding:utf-8 -*- 
# --------------------
# Author:       SDN
# Description:	将时间转换成各种需要
# Time:         2017/3/13
# --------------------

import time

import datetime


def time_id():
    """
    1488895269.76 -> 148889526976, 作为id用
    :return:
    """
    # return int(str(time.time()).replace('.', ''))
    return int(str(time.time()).replace('.', ''))


def time_name():
    """
        1488895269.76 -> 148889526976, 作为名字用
        :return:
        """
    # return int(str(time.time()).replace('.', ''))
    return str(time.time()).replace('.', '')


def datetime_name_full():
    """
        以当前时间转字符串：20170307203810929000
        :return:
        """
    result = ''
    for item in str(datetime.datetime.now()):
        try:
            int(item)
            result += item
        except Exception as e:
            pass
    # return str(datetime.datetime.now()).replace('-', '').replace(' ', '').replace(':', '').replace('.', '')
    return result


def datetime_name_simple():
    """
    20170316235852
    :return:
    """
    result = ''
    temp = str(datetime.datetime.now()).split('.')[0]
    for item in temp:
        try:
            int(item)
            result += item
        except Exception as e:
            pass
    return result


def datetime_date_full():
    """
    2017-03-07 22:24:55.510000
    :return:
    """
    return str(datetime.datetime.now())


def datetime_date_simple():
    """
    2017-03-07 22:24:55
    :return:
    """
    return str(datetime.datetime.now()).split('.')[0]


def simplify_date(date_full):
    """
    将完整时间变成简单显示：2017-03-07 22:24:55.510000 to 2017-03-07 22:24:55
    :return:
    """
    date_full = str(date_full)
    if date_full and len(date_full) > 5:
        return date_full.split('.')[0]
    else:
        return ''


def format_date(date_str):
    """
    2017-03-08 10:21:11, or 2017-03-08 10:21:11.23486 转为 2017年3月3日
    :param date_str:    数据库查出来的数据是 unicode
    :return:
    """
    try:
        if date_str:
            if isinstance(date_str, type(u'')):
                temp = date_str.encode('utf-8')
            else:
                temp = date_str
            temp = temp.split(' ')[0]
            temp = temp.split('-')
            result = temp[0] + '年'
            if temp[1].startswith('0'):
                result = result + temp[1][1:] + '月'
            else:
                result = result + temp[1] + '月'

            if temp[2].startswith('0'):
                result = result + temp[2][1:] + '日'
            else:
                result = result + temp[2] + '日'
            return result
        else:
            return ''
    except Exception as e:
        print __name__, "format_date exception: ", e
        return ''



if __name__ == '__main__':
    print datetime_name_full()
    print datetime_name_simple()
