# -*- coding:utf-8 -*-
"""
图片相关的操作：压缩、水印、缩略图
"""
import os
import traceback

import math
from PIL import Image


FIT_WIDTH_AND_HEIGHT = 0
FIT_WIDTH = 1
KEEP_RADIO = 2


# 添加水印
def add_watermark_to_image(image_file_path, watermark_image_path, opacity=50):
    image = Image.open(image_file_path)
    watermark = Image.open(watermark_image_path)

    rgba_image = image.convert('RGBA')
    rgba_watermark = watermark.convert('RGBA')

    # 旋转水印图片
    watermark_x, watermark_y = rgba_watermark.size
    watermark_size = int(
        math.sqrt(watermark_x * watermark_x + watermark_y * watermark_y))
    watermark = Image.new('RGBA', (watermark_size, watermark_size), (0, 0, 0,
                                                                     0))
    water_center = int(watermark_size // 2)
    water_or_x = int(watermark_x // 2)
    water_or_y = int(watermark_y // 2)
    watermark.paste(rgba_watermark, (water_center - water_or_x,
                                     water_center - water_or_y))
    # 缩放图片
    rgba_watermark = watermark.rotate(45).resize((200, 200))
    # 透明度
    al = rgba_watermark.convert("L").point(lambda x: min(x, opacity))
    rgba_watermark.putalpha(al)

    # rgba_watermark.save(DEFAULT_WATERMARK_PATH)

    watermark_x, watermark_y = rgba_watermark.size
    # 水印位置
    image_x, image_y = rgba_image.size
    horizon_num = image_x / watermark_x + 1
    vertical_num = image_y / watermark_y + 1

    for h in range(horizon_num):
        for v in range(vertical_num):
            rgba_image.paste(rgba_watermark, (h * 200, v * 200), al)

    if image.format == "PNG":
        # rgba_image.paste(rgba_watermark, (image_x - watermark_x, image_y - watermark_y), al)
        rgba_image.save(image_file_path)
    else:
        r, g, b, a = rgba_image.split()
        target_image = Image.merge("RGB", (r, g, b))
        target_image.save(image_file_path)


# 压缩图片
def compress_quality(image_file_path, quality_limit):
    """

    :param image_file_path: 图片路径
    :param quality_limit: 图片保存质量
    :return:
    """
    path_split = os.path.splitext(image_file_path)
    if len(path_split) > 1:
        file_suffix = path_split[1]
        if file_suffix not in ['.png', '.PNG']:
            Image.open(image_file_path).save(
                image_file_path, quality=quality_limit)


def compress_size(image_file_path, size_limit):
    """

    :param image_file_path:
    :param size_limit:
    :return:
    """
    path_split = os.path.splitext(image_file_path)
    if len(path_split) > 1:
        file_suffix = path_split[1]
        if file_suffix not in ['.png', '.PNG']:
            limit_size = size_limit * 1000
            pass


def compress_image_keep_radio(image_file_path, width_limit, height_limit,
                              quality):
    """
    对图片进行尺寸压缩， 如果图片为jpg，按制定质量保存
    :param image_file_path:
    :param quality: jpg保存质量
    :param width_limit:     宽限制
    :param height_limit:    高限制
    :return:
    """
    img = Image.open(image_file_path)
    dst_w = width_limit
    dst_h = height_limit
    file_path = image_file_path

    ori_w, ori_h = img.size
    widthRatio = heightRatio = None
    ratio = 1

    if (ori_w and ori_w > dst_w) or (ori_h and ori_h > dst_h):
        if dst_w and ori_w > dst_w:
            widthRatio = float(dst_w) / ori_w  # 正确获取小数的方式
        if dst_h and ori_h > dst_h:
            heightRatio = float(dst_h) / ori_h

        if widthRatio and heightRatio:
            if widthRatio < heightRatio:
                ratio = widthRatio
            else:
                ratio = heightRatio

        if widthRatio and not heightRatio:
            ratio = widthRatio

        if heightRatio and not widthRatio:
            ratio = heightRatio

        newWidth = int(ori_w * ratio)
        newHeight = int(ori_h * ratio)
    else:
        newWidth = ori_w
        newHeight = ori_h
    img.resize((newWidth, newHeight), Image.ANTIALIAS).save(
        file_path, quality=quality)


def compress_image_to_given_width(image_file_path,
                                  width_limit,
                                  quality_limit=0,
                                  size_limit=0,
                                  enforce=False):
    """
    把图片的宽度压缩到指定值，高按比例
    :param enforce: False 宽小于制定值就不压缩
    :param size_limit: 图片大小
    :param quality_limit: 图片子良
    :param image_file_path: 图片绝对路径
    :param width_limit: 图片目标宽度
    :return:
    """
    image_obj = Image.open(image_file_path)
    if enforce:
        img_resize = image_obj.resize((width_limit, int(
            (float(width_limit) / image_obj.size[0]) * image_obj.size[1])),
                                      Image.ANTIALIAS)
        img_resize.save(image_file_path)
    else:
        if image_obj.size[0] > width_limit:
            img_resize = image_obj.resize((width_limit, int(
                (float(width_limit) / image_obj.size[0]) * image_obj.size[1])),
                                          Image.ANTIALIAS)
            img_resize.save(image_file_path)
    if quality_limit > 0:
        compress_quality(image_file_path, quality_limit)
    elif size_limit > 0:
        compress_size(image_file_path, size_limit)
    return os.path.getsize(image_file_path)


def compress_image_to_given_dimension(image_file_path,
                                      height_limit,
                                      width_limit,
                                      quality_limit=0,
                                      size_limit=0):
    """
    将图片压缩到指定的大小
    :param image_file_path: 图片文件保存路径
    :param height_limit: 图片高度限制
    :param width_limit: 图片宽度限制
    :param quality_limit: >0 的jpg图片要保存质量
    :param size_limit:
    :return: 返回压缩后的图片大小
    """
    image_file = Image.open(image_file_path)
    image_resize = image_file.resize((width_limit, height_limit),
                                     Image.ANTIALIAS)
    image_resize.save(image_file_path)
    if quality_limit > 0:
        compress_quality(image_file_path, quality_limit)
    elif size_limit > 0:
        compress_size(image_file_path, size_limit)
    return os.path.getsize(image_file_path)


def compress_image(image_file_path,
                   compress_type=0,
                   width_limit=1024,
                   height_limit=768,
                   quality_limit=85,
                   size_limit=0,
                   enforce=False,
                   watermark=False):
    """

    :param enforce:
    :param image_file_path: 图片文件路径
    :param compress_type: 压缩方式
    :param width_limit: 宽限
    :param height_limit: 高限
    :param quality_limit: jpg质量限制
    :param size_limit: 大小限制
    :return:
    """
    if compress_type == 0:  # 宽高到指定值
        compress_image_to_given_dimension(image_file_path, height_limit,
                                          width_limit, quality_limit,
                                          size_limit)
    elif compress_type == 1:  # 宽到指定值
        compress_image_to_given_width(image_file_path, width_limit,
                                      quality_limit, size_limit, enforce)
    elif compress_type == 2:  #
        compress_image_keep_radio(image_file_path, width_limit, height_limit,
                                  quality_limit)
    else:  # 宽到指定值
        compress_image_to_given_width(image_file_path, width_limit,
                                      quality_limit, size_limit, enforce)
    if watermark:
        add_watermark_to_image(image_file_path, DEFAULT_WATERMARK_PATH)
    return os.path.getsize(image_file_path)


# 创建缩略图
def create_thumbnail(image_file_path,
                     thumb_save_path,
                     thumb_width,
                     thumb_height,
                     enforce=True):
    """
    创建缩略图
    :param enforce: True 按给定尺寸生成缩略图
    :param image_file_path: 源文件路径
    :param thumb_save_path: 缩略图保存路径
    :param thumb_width:
    :param thumb_height:
    :return:
    """

    def clipimage(image_width, image_height, ratio):
        """
        1、取宽和高的值小的那一个来生成裁剪图片用的box
        2、尽可能的裁剪出图片的中间部分,一般人摄影都会把主题放在靠中间的,个别艺术家有特殊的艺术需求顾不上
        :param image_width:
        :param image_height:
        :param ratio:
        :return:
        """
        if image_width > image_height:
            dx = image_width - image_height
            c_box = (dx / 2, 0, image_height + dx / 2, image_height)
        else:
            dx = image_height - image_width
            c_box = (0, dx / 2, image_width, image_width + dx / 2)
        return c_box

    image_obj = Image.open(image_file_path)
    image_size = image_obj.size

    if enforce:
        image_obj = Image.open(image_file_path)
        image_resize = image_obj.resize((thumb_width, thumb_height),
                                        Image.ANTIALIAS)
        image_resize.save(thumb_save_path)
        return os.path.getsize(thumb_save_path)

    if (image_size[0] < thumb_width) & (image_size[1] < thumb_height):
        image_obj.thumbnail((thumb_width, thumb_height), Image.ANTIALIAS)
        image_obj.save(thumb_save_path, format='jpeg')
        return os.path.getsize(thumb_save_path)

    box = clipimage(image_size[0], image_size[1],
                    thumb_height / float(thumb_width))
    region = image_obj.crop(box)  # 裁切图片
    region.thumbnail((thumb_width, thumb_height), Image.ANTIALIAS)  # 生成缩略图
    region.save(thumb_save_path, format='jpeg')
    return os.path.getsize(thumb_save_path)
