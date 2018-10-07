# -*- coding: utf-8 -*-
# !/usr/bin/env python
# --------------------
# Author:       Yh
# Description:  生成原始图片的缩略图
# --------------------

import os
from PIL import Image
from PIL import ImageFile


def thumb_logo(imgFile, outputDir, thumb_width=200, thumb_height=200):
    """
    imgFile 原始图片文件路径
    在原始图片目录，新建thumb文件夹作为缩略图存放文件夹
    size是缩略图计划的长宽尺寸

    如果size=500，图片是600*400的，缩略图最后size是400
    :param imgFile: 原始图片的路径
    :param outputDir: 输出缩略图的路径
    :return: 缩略大小
    """
    # print imgFile
    ImageFile.LOAD_TRUNCATED_IMAGES = True  # 不加会抛出：image file is truncated
    im = imgFile
    try:
        if (im.size[0] < thumb_width) & (im.size[1] < thumb_height):
            raise Exception('图片原始尺寸小于生成缩略图的size，出错')
    except Exception, e:
        print "Error: %s" % e

    ratio = thumb_height / float(thumb_width)

    box = clipimage(im.size, ratio)
    region = im.crop(box)  # 裁切图片
    _size = (thumb_width, thumb_height)
    region.thumbnail(_size, Image.ANTIALIAS)  # 生成缩略图
    region.save(outputDir)
    return os.path.getsize(outputDir)


def thumb2(imgFile, outputDir, thumb_width=200, thumb_height=200):
    """
    imgFile 原始图片文件路径
    在原始图片目录，新建thumb文件夹作为缩略图存放文件夹
    size是缩略图计划的长宽尺寸

    如果size=500，图片是600*400的，缩略图最后size是400
    :param imgFile: 原始图片的路径
    :param outputDir: 输出缩略图的路径
    :return: 缩略大小
    """
    # print imgFile
    ImageFile.LOAD_TRUNCATED_IMAGES = True  # 不加会抛出：image file is truncated
    im = imgFile
    try:
        if (im.size[0] < thumb_width) & (im.size[1] < thumb_height):
            raise Exception('图片原始尺寸小于生成缩略图的size，出错')
    except Exception, e:
        print "Error: %s" % e

    ratio = thumb_height / float(thumb_width)

    box = clipimage(im.size, ratio)
    region = im.crop(box)  # 裁切图片
    _size = (thumb_width, thumb_height)
    region.thumbnail(_size, Image.ANTIALIAS)  # 生成缩略图
    region.save(outputDir, format='jpeg')
    return os.path.getsize(outputDir)


def thumb(imgFile, outputDir, thumb_width=200, thumb_height=200):
    """
    imgFile 原始图片文件路径
    在原始图片目录，新建thumb文件夹作为缩略图存放文件夹
    size是缩略图计划的长宽尺寸

    如果size=500，图片是600*400的，缩略图最后size是400
    :param imgFile: 原始图片的路径
    :param outputDir: 输出缩略图的路径
    :param size: 缩略图的尺寸
    :return: 缩略图保存的路径
    """
    # print imgFile
    ImageFile.LOAD_TRUNCATED_IMAGES = True  # 不加会抛出：image file is truncated
    try:
        im = Image.open(imgFile)
        if (im.size[0] < thumb_width) & (im.size[1] < thumb_height):
            raise Exception('图片原始尺寸小于生成缩略图的size，出错')
    except Exception, e:
        print "Error: %s" % e

    ratio = thumb_height / float(thumb_width)

    box = clipimage(im.size, ratio)
    region = im.crop(box)  # 裁切图片
    _size = (thumb_width, thumb_height)
    region.thumbnail(_size, Image.ANTIALIAS)  # 生成缩略图
    region.save(outputDir)
    return outputDir


def clipimage(size, ratio):
    """
    1、取宽和高的值小的那一个来生成裁剪图片用的box
    2、尽可能的裁剪出图片的中间部分,一般人摄影都会把主题放在靠中间的,个别艺术家有特殊的艺术需求顾不上
    :param size:
    :return:
    """
    width = int(size[0])
    height = int(size[1])
    # if int(ratio*width) <= height:
    #     pass
    # else:
    #     pass

    box = ()
    if width > height:
        dx = width - height
        box = (dx / 2, 0, height + dx / 2, height)
    else:
        dx = height - width
        box = (0, dx / 2, width, width + dx / 2)
    return box


def getFilenameAndExt(filename):
    """

    :param filename: "D://12//345.jpg"
    :return: 返回文件名（345），扩展名(.jpg)
    """
    (filepath, tmpfilename) = os.path.split(filename)
    (shotname, extension) = os.path.splitext(tmpfilename)
    return shotname, extension

# print getFilenameAndExt("D://12//345.jpg")
# print thumb("1234.jpg")
# print thumb("D://123.jpg")
