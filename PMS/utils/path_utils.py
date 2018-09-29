#!/usr/bin/env python
# -*- coding:utf-8 -*-
# --------------------
# Author:       SDN
# Description:  文件路径相关的工具类
# --------------------
import os
import platform


def path_none_system(path_origin, use_unicode=False):
    """
    将给定的路径字符串，变为系统无关
    :param use_unicode: True 返回unicode， False 返回 str
    :param path_origin:   给定的路径是相对路径，不是绝对路径
    :return:   去除了首尾的路径符号
    """
    path_temp = path_origin
    driver_tag = ''
    if isinstance(path_origin, type(u'')):
        path_temp = path_origin.encode('utf-8')  # 变为 str 操作
    if platform.system() == 'Windows' and ':' in path_temp:
        driver_tag = path_temp.split(':')[0]
        path_temp = path_temp.split(':')[1]
    path_temp = path_temp.replace('\\\\', '|').replace('\\', '|').replace(
        '/', '|')
    if path_temp.startswith('|'):
        path_temp = path_temp[1:]
    if path_temp.endswith('|'):
        path_temp = path_temp[:-1]
    path_temp = path_temp.split('|')
    result = ''
    for item in path_temp:
        result = os.path.join(result, item)
    if driver_tag != '' and platform.system() == 'Windows':
        result = driver_tag + ':\\' + result
    if use_unicode:
        return result.decode('utf-8')
    else:
        return result


def get_file_suffix(path):
    """
    获得文件的后缀
    :param path:
    :return:
    """
    return (os.path.splitext(path))[1]


def to_url(path):
    """
    将路径转换为 url 路径， 数据库中保存的文件路径均为 url 格式的路径（不包括静态文件名）
    :param path:
    :return:
    """
    if '|' not in path:
        return path.replace('\\', '|').replace('\\\\',
                                               '|').replace('/', '|').replace(
            '|', "/")


def connect(*path_list):
    """
    os.path.join在组装路径时，如果编码不同，会异常（在有中文时）
    :param path_list:    要连接的其他路径
    :return:
    """
    if len(path_list) == 0:
        return ''
    if len(path_list) == 1:
        if isinstance(path_list[0], type(u'')):
            return path_list[0].encode('utf-8')
        else:
            return path_list[0]
    # 全转为字符串
    result = ''
    for item in path_list:
        if item is None:
            item = ''
        elif isinstance(item, type(u'')):
            item = item.encode('utf-8')
        else:
            item = str(item)
        result = os.path.join(result, item)
    return result


def connect0(path_static, *path_list):
    """
    os.path.join在组装路径时，如果编码不同，会异常（在有中文时）
    :param path_static: 静态文件夹路径（不能包含中文）
    :param path_list:    要连接的其他路径
    :return:
    """
    if path_static and len(path_list) > 0:

        # 全转为字符串
        if isinstance(path_static, type(u'')):
            result = path_static.encode('utf-8')
        else:
            result = path_static
        for item in path_list:
            if item is None:
                item = ''
            elif isinstance(item, type(u'')):
                item = item.encode('utf-8')
            elif isinstance(item, type(1)):
                item = str(item)
            elif isinstance(item, type(0.1)):
                item = str(item)
            result = os.path.join(result, item)
        return result
    else:
        if path_static is None:
            return ''
        else:
            if isinstance(path_static, type(u'')):
                return path_static.encode('utf-8')
            else:
                return path_static


def format_folder_path(folder_path):
    """
    将传入的文件夹路径转换成系统无关的输出
    :param folder_path: 文件夹路径, 路径不能有盘符，盘符单独写
    :return:
    """
    if "|" not in folder_path:
        folder_path = folder_path.replace('/', '|').replace('\\', '|').replace(
            '\\\\', '|')

        if folder_path.startswith('|'):
            folder_path = folder_path[1:]

        if folder_path.endswith('|'):
            folder_path = folder_path[:-1]

        folder_path = folder_path.split('|')
        path_folder = ''
        # 得到文件夹的相对路径（系统无关）
        for item in folder_path:
            path_folder = os.path.join(path_folder, item)
        return path_folder
    else:
        return None


def get_folder_list(path_absolute):
    """
    获取制定路径下，文件夹列表, 包括次级目录
    :param path_absolute: 路径为绝对路径
    :return:
    """
    path_exist = os.path.exists(path_absolute)
    if not path_exist:
        raise Exception('path not exist')
    is_directory = os.path.isdir(path_absolute)
    if not is_directory:
        raise Exception('path not dir')

    all_dir = os.listdir(path_absolute)

    # 只要文件夹
    path_list = []
    for item in all_dir:
        if os.path.isdir(os.path.join(path_absolute, item)):
            path_list.append(item)
            result = get_folder_list(os.path.join(path_absolute, item))
            path_list += result
        # else:
        #     path_list.append(os.path.join(path_absolute, item))
    return path_list


def get_file_list(path_absolute, filter_list=None):
    """
    获取制定路径下，文件列表
    :param filter_list: 筛选文件，　文件后缀列表
    :param path_absolute: 路径为绝对路径
    :return:
    """
    path_exist = os.path.exists(path_absolute)
    if not path_exist:
        raise Exception('path not exist')
    is_directory = os.path.isdir(path_absolute)
    if not is_directory:
        raise Exception('path not dir')

    all_dir = os.listdir(path_absolute)

    # 只要文件
    file_list = []
    for item in all_dir:
        absolute_path_ = os.path.join(path_absolute, item)
        if os.path.isfile(absolute_path_):
            if filter_list:
                suffix = os.path.splitext(absolute_path_)[1]
                if suffix in filter_list:
                    file_list.append(absolute_path_)
            else:
                file_list.append(item)
        else:
            result = get_file_list(absolute_path_, filter_list)
            file_list += result
    return file_list


if __name__ == '__main__':
    path_ = '/home/super/Desktop/1'
    import pprint

    pprint.pprint(get_file_list(path_, ['.png', '.jpeg', '.jpg', '.mp4']))
