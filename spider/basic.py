# -*- coding:utf-8 -*-
# --------------------
# Author:   SDN
# Description:	第一个爬虫示例
# 文件管理/数据存储
# ----------------
import cookielib
import logging
import traceback
import urllib
import urllib2
import re

import datetime

import os


def save_web_content(file_path, web_content):
    """
    保存网页内容到文件
    :param file_path:
    :param web_content:
    :return:
    """
    with open(file_path, mode="wb") as save_file:
        save_file.write(web_content)


def get_date_path():
    """
    以当前日期生成路径
    :return: 2017/12/16
    """
    now_datetime = datetime.datetime.now()
    now_year = now_datetime.year
    now_month = now_datetime.month
    now_day = now_datetime.day
    return '{0}/{1}/{2}'.format(now_year, now_month, now_day)


def save_file(file_path, file_url):
    """

    :param file_path: 文件保存的路径
    :param file_url: 文件的url路径
    :return:
    """


def crawling():
    """
    爬取
    :return:
    """
    website_base_url = "http://localhost:9003"
    admin_login_url = website_base_url + '/admin/login'

    # 获取网页内容
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36"
    }
    request = urllib2.Request(url=web_url, headers=headers)

    response = urllib2.urlopen(request)
    web_content = response.read()
    # 从网页内容中正则图片路径
    re_pattern = re.compile(r'<img src=".*?"')
    image_paths_temp = re_pattern.findall(web_content)
    image_paths = list(set(image_paths_temp))  # 去重
    for index, item in enumerate(image_paths):
        image_paths[index] = item.replace('<img src="', '').replace('"', '')

    # 从url获取图片
    for image_path in image_paths:
        file_name = os.path.basename(image_path)
        if image_path.startswith('http'):
            try:
                urllib.urlretrieve(image_path, file_name)
            except:
                traceback.print_exc()
        else:
            image_url = os.path.join(website_base_url, image_path[1:])
            try:
                urllib.urlretrieve(image_url, file_name)
            except:
                traceback.print_exc()


def get_zihu_home():
    url = "http://localhost:9003/admin/login"
    # -------- 设置代理
    enable_proxy = False
    proxy_handler = urllib2.ProxyHandler({
        'http': 'http://199.11.11.1:8080',
    })
    null_proxy_handler = urllib2.ProxyHandler({})
    if enable_proxy:
        opener = urllib2.build_opener(proxy_handler)
    else:
        opener = urllib2.build_opener(null_proxy_handler)
    urllib2.install_opener(opener)
    # ---------- debug log（测试日志）
    httphandler = urllib2.HTTPHandler(debuglevel=1)
    httpshandler = urllib2.HTTPSHandler(debuglevel=1)
    opener2 = urllib2.build_opener(httphandler, httpshandler)
    urllib2.install_opener(opener2)
    # ---------- request
    headers = {

    }
    data = {
        "username": 'admin',
        "password": '123456'
    }
    request = urllib2.Request(url, headers=headers, data=urllib.urlencode(data))
    # ---------- 请求数据
    try:
        response = urllib2.urlopen(request, timeout=3)
        save_web_content('zhihuhome.html', response.read())
        print response.url
    except:
        traceback.print_exc()


def save_cookie_to_var():
    """
    把cookie保存到变量
    :return:
    """
    url = "http://localhost:9000/manage"
    # url = "http://www.baidu.com"
    # 准备cookie handler
    cookie_receiver = cookielib.MozillaCookieJar()
    handler_cookie_file = urllib2.HTTPCookieProcessor(cookie_receiver)
    opener = urllib2.build_opener(handler_cookie_file)
    urllib2.install_opener(opener)
    # 1、get，获取_xsrf
    headers1 = {}
    request1 = urllib2.Request(url, headers=headers1)
    response1 = urllib2.urlopen(request1, timeout=10)
    save_web_content('admin_login.html', response1.read())
    cookie_receiver.save(filename='get_cookie.txt', ignore_discard=True, ignore_expires=True)
    _xsrf = ''
    for item in cookie_receiver:
        if item.name == '_xsrf':
            _xsrf = item.value
    # 2、post登录，获取登录cookie
    data = urllib.urlencode({
        'name_login': 'admin',
        'ps_login': '654321',
        '_xsrf': _xsrf
    })
    url_login = url + '/login'
    request2 = urllib2.Request(url_login, data=data)
    response2 = urllib2.urlopen(request2)
    save_web_content('admin_login_data.html', response2.read())
    cookie_receiver.save(filename='post_cookie.txt', ignore_discard=True, ignore_expires=True)
    # 3、访问其他网页
    response3 = urllib2.urlopen(url)
    save_web_content('manage.html', response3.read())




if __name__ == '__main__':
    save_cookie_to_var()
