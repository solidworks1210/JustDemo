# -*- coding:utf-8 -*-
# --------------------
# Author:   SDN
# Description:	基于python2.7
# ----------------
import urllib2
import urllib


# urllib2 获取网页内容
def get_web_content():
    """
    urllib2 获取网页内容
    :return:
    """
    target_url = 'https://www.baidu.com'
    headers = {

    }
    request = urllib2.Request(target_url, headers=headers)
    response = urllib2.urlopen(request)
    return response.read()


# urllib 获取文件（静态文件）
def get_file_from_web():
    """
    urllib 获取文件
    :return:
    """
    url = ''
    file_save_path = ''
    urllib.urlretrieve(url, file_save_path)

# urllib2 模拟登录