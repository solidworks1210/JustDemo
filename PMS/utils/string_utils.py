# -*- coding:utf-8 -*- 
# --------------------
# Author:       SDN
# Description:	字符串操作相关
# --------------------
import random


def connect(*args):
    """
    拼接字符串：
    与join不同，改方法忽略编码、类型
    sd = [1, 'ad', u's中']， join会报错， 不能join不同类型
    'sdf{0}'.format(u'中')， 报编码不对
    :return: 字符串
    """
    if len(args) > 0:
        result = ''
        # 全转为字符串
        for item in args:
            if isinstance(item, type(u'')):  # unicode
                item = item.encode('utf-8')
            elif isinstance(item, type(1)):  # 数字
                item = str(item)
            elif isinstance(item, type(0.1)):  # 小数
                item = str(item)
            elif isinstance(item, type(3L)):
                item = str(item)
            result += item
        return result
    else:
        raise AttributeError('Nothing to connect')


def create_random_number_string(length):
    """

    :param length: 输出的字符串长度
    :return:
    """
    if not isinstance(length, type(1)):
        raise AttributeError('length must be int')
    _max = int('9' * length)
    _min = int('1' + '0' * (length - 1))
    return str(random.randint(_min, _max))


if __name__ == '__main__':
    print 'sdf{0}'.format(u'中')
