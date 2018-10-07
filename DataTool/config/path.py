# -*- coding:utf-8 -*- 
# --------------------
# Author:       SDN
# Description:	各种路径
# Time:         2017/3/16
# --------------------

import os

# 静态文件夹名字
from utils import PathUtils
from utils import StringUtils

NAME_STATIC = 'static'
# 模板文件名
NAME_TEMPLATE = 'templates'
# 文件存放 根目录的名字
NAME_FILE_ROOT = 'files'

# 项目根目录
PATH_BASE = os.path.dirname(os.path.dirname(__file__))
# 静态资源目录
PATH_STATIC = os.path.join(PATH_BASE, NAME_STATIC)
# 模板路径
PATH_TEMPLATE = os.path.join(PATH_BASE, NAME_TEMPLATE)


# 以下路径都是不含静态文件夹名的相对路径
# 默认使用文件路径保存的路径（files/default/）(该文件夹下放：默认logo、默认缩略图、验证码图片)
PATH_DEFAULT_FILE = os.path.join(NAME_FILE_ROOT, 'default')
# 上传文件的路径（files/upload/）
PATH_UPLOAD = os.path.join(NAME_FILE_ROOT, 'upload')    # 这样写系统相关，使用时要通过os.path.join转为系统无关
# 临时文件存放夹(该文件夹可随意删)(files/temp/)
# PATH_TEMP = os.path.join(NAME_FILE_ROOT, 'temp')
PATH_TEMP = os.path.join(PATH_STATIC, NAME_FILE_ROOT, 'temp')
# 上传的 logo 保存的路径(保存在 upload 文件夹下)
PATH_LOGO = 'logo'

# 默认缩略图路径（不含静态文件夹名，url 形式）
PATH_THUMB_DEFAULT = 'files/default/default_thumb.jpg'
# 默认logo文件的路径（数据库没有内容时用）
PATH_LOGO_DEFAULT = 'files/default/logo.png'


# 验证码存放相对路径
PATH_VERIFY_SAVE_RELATIVE = PathUtils.connect(PATH_STATIC, 'files/default')
# 验证码存放绝对路径
PATH_VERIFY_SAVE_ABSOLUTE = PathUtils.connect(PATH_STATIC, 'files/default/verify.jpg')
# 验证码网页使用路径
PATH_VERIFY_URL = StringUtils.connect('/', NAME_STATIC, '/', 'files/default/verify.jpg')
# 验证码字体文件路径
PATH_VERIFY_FONT = PathUtils.connect(PATH_STATIC, 'files/default/Monaco.ttf')
