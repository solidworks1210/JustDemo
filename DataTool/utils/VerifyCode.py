# -*- coding:utf-8 -*-
# --------------------
# Author:
# Description:	生成验证码: 根据一个任意的四位字符串，生成验证码
# Time:         2017/3/13
# --------------------
import os
import random
import time

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont


def time_name():
    """
    1488895269.76 -> 148889526976
    :return:
    """
    return str(time.time()).split('.')[0]


# 随机字母:
def randChar():
    return chr(random.randint(65, 90))


# 随机颜色1:
def randColor():
    return (random.randint(64, 255), random.randint(64, 255), random.randint(64, 255))


# 随机颜色2:
def randColor2():
    return (random.randint(32, 127), random.randint(32, 127), random.randint(32, 127))


def create(font_path):
    """
    :return: 返回验证码保存的路径，生成验证码的原始字符串
    :static_path: 静态文件路径
    :save_path: 'static/files/images/verify'
    :name: 文件名
    """
    # 240 x 60:
    width = 60 * 4
    height = 60
    image = Image.new('RGB', (width, height), (255, 255, 255))
    # 创建Font对象:
    font = ImageFont.truetype(font_path, 36)
    # font = ImageFont.truetype('utils/Monaco.ttf', 36)
    # 创建Draw对象:
    draw = ImageDraw.Draw(image)
    # 填充每个像素:
    for x in range(width):
        for y in range(height):
            draw.point((x, y), fill=randColor())
    # 输出文字:
    code_string = ''
    for t in range(4):
        char = randChar()
        draw.text((60 * t + 10, 10), char, font=font, fill=randColor2())
        code_string += char
    # 模糊:
    # image = image.filter(ImageFilter.BLUR)

    # # 保存
    # path_to_folder = STATIC_PATH + Q_VERIFY_PATH
    # path_to_file = path_to_folder + '\\' + 'verify' + '.jpg'
    # try:
    #     image.save(path_to_file, 'jpeg')
    # except:
    #     # 保存路径不存在，创建
    #     if not os.path.exists(path_to_folder):
    #         os.makedirs(path_to_folder)
    #     image.save(path_to_file, 'jpeg')
    return image, code_string

