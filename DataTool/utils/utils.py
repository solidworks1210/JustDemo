# coding: utf-8
import time

import datetime
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import random
import os
from config import config

save_path = 'static/files/images/verify/verify.jpg'


# class VerifyCode:
#     # 随机字母:
#     def randChar(self):
#         return chr(random.randint(65, 90))
#
#     # 随机颜色1:
#     def randColor(self):
#         return (random.randint(64, 255), random.randint(64, 255), random.randint(64, 255))
#
#     # 随机颜色2:
#     def randColor2(self):
#         return (random.randint(32, 127), random.randint(32, 127), random.randint(32, 127))
#
#     def create(self):
#         # 240 x 60:
#         width = 60 * 4
#         height = 60
#         image = Image.new('RGB', (width, height), (255, 255, 255))
#         # 创建Font对象:
#         font = ImageFont.truetype('utils/Monaco.ttf', 36)
#         # 创建Draw对象:
#         draw = ImageDraw.Draw(image)
#         # 填充每个像素:
#         for x in range(width):
#             for y in range(height):
#                 draw.point((x, y), fill=self.randColor())
#         # 输出文字:
#         code_string = ''
#         for t in range(4):
#             char = self.randChar()
#             draw.text((60 * t + 10, 10), char, font=font, fill=self.randColor2())
#             code_string = code_string + char
#         # 模糊:
#         # image = image.filter(ImageFilter.BLUR)
#         # 保存
#         try:
#             image.save(save_path, 'jpeg')
#         except:
#             path = save_path.split('.')[0]
#             os.makedirs(path)
#             os.mknod(save_path)
#             image.save(save_path, 'jpeg')
#         return image, code_string


# 按指定方式将明文验证码混淆
def mix_string(string):
    result = string
    return result


# 按指定的方式将混淆后的验证码变为明文
def un_mix(string):
    result = string
    return result


# 当前时间的浮点数形式，取整数部分
def number():
    return int(str(time.time()).split('.')[0])


# 这个方法把要写入数据库的数据进行格式化：1、使sql语句合法；2、防sql注入攻击
def clean_content(content):
    result = content
    if content is not None and content != '':
        result = result.replace("%", "#$&")
        result = result.replace("'", "&*#")
    return result


# 将从数据库获得的数据还原为原始状态
def recovery_content(content):
    result = content
    if content is not None and content != '':
        result = result.replace("#$&", "%")
        result = result.replace("&*#", "'")
    return result


def time_int():
    """
    1488895269.76 -> 148889526976, 作为id用
    :return:
    """
    # return int(str(time.time()).replace('.', ''))
    return int(str(time.time()).split('.')[0])


def datetime_now_simple():
    """
    2017-03-07 22:24:55
    :return:
    """
    return str(datetime.datetime.now()).split('.')[0]


def datetime_now_full():
    """
    2017-03-07 22:24:55.510000
    :return:
    """
    return str(datetime.datetime.now())


def time_to_str():
    """
    以当前时间转字符串：20170307203810929000
    :return:
    """
    result = ''
    for item in str(datetime.datetime.now()):
        try:
            int(item)
            result += item
        except:
            pass
    # return str(datetime.datetime.now()).replace('-', '').replace(' ', '').replace(':', '').replace('.', '')
    return result


def time_to_int():
    """
    把时间转为数字：20170307203810929000
    :return:
    """
    result = ''
    for item in str(datetime.datetime.now()):
        try:
            int(item)
            result += item
        except:
            pass
    # return str(datetime.datetime.now()).replace('-', '').replace(' ', '').replace(':', '').replace('.', '')
    return int(result)


def str_time():
    """
    将当前时间转为字符串：2017-03-07 20:43:06.513000
    :return:
    """
    return str(datetime.datetime.now())


def formate_date(date_str):
    """
    2017-03-08 10:21:11, 转为 2017年3月3日
    :param date_str:    数据库查出来的数据是 unicode
    :return:
    """
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


def get_first_image_in_html(content):
    """
    获取自定义网页中的第一幅图片
    :param content:
    :return:
    """
    if type(content) == type(u''):
        temp = content.encode('utf-8')
    else:
        temp = content
    temp = temp.split('<img src=')
    if len(temp) < 2:
        return config.DEFAULT_IMAGE
    temp = temp[1]
    temp = temp.split('"')
    if len(temp) > 1:
        return temp[1]
    else:
        return config.DEFAULT_IMAGE


def get_all_image_path_in_content(content):
    """
    获取自定义页面中所有图片的路径
    :param content:
    :return:
    """
    if type(content) == type(u''):
        temp = content.encode('utf-8')
    else:
        temp = content
    temp = temp.split('<img src=')[1:]
    image_path = []
    for item in temp:
        image_path.append(item.split('"')[1])
    return image_path




if __name__ == '__main__':
    # print time_to_name()
    # print str_time()
    # print time_int()
    # print formate_date('2017-03-08 10:21:11')
    s = """

<p><img src="/static/files/images/20170314221039681000.jpg" alt="197268260890988455" style="max-width: 100%; width: 547px; height: 233px;" class=""><br></p><p><br></p><p>gosfsa</p><p>sdfsa</p><p><img src="/static/files/images/20170314221112960000.jpg" alt="8" style="max-width: 100%; width: 198px; height: 264px;" class=""><br></p><p><img src="/static/files/images/20170314221123664000.jpg" alt="10" style="max-width:100%;"><br></p>
<p><br></p>
    """
    get_all_image_path_in_content(s)
