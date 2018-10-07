# -*- coding:utf-8 -*- 
# --------------------
# Author:       SDN
# Description:	
# Time:         2017/4/6
# --------------------
import os

from PIL import Image


def fit_dimension_from_image_file(image_file, image_type, save_path, height_limit, width_limit, quality):
    try:
        print __name__, '调到给定大小：', width_limit, height_limit
        print __name__, '图片尺寸：', image_file.size
        save_image = image_file.resize((width_limit, height_limit), Image.ANTIALIAS)

        # if image_type == 'image/jpeg':
        #     print __name__, '图片是jpg，压缩质量：', quality
        #     save_image.save(save_path, quality=quality)
        # else:
        #     print __name__, '图片不是jpg'
        #     save_image.save(save_path)
        save_image.save(save_path, format='jpeg', quality=quality)

        result_size = os.path.getsize(save_path)
        print __name__, '最终图片：', save_image.size, result_size / 1024.0
        return result_size
    except Exception as e:
        print __name__, '对图片进行尺寸压缩出错：', e
        return 0


def compress_image_file_by_height_limit(image_file, image_type, save_path, height_limit, quality):
    try:
        print __name__, '高限制：', height_limit
        print __name__, '图片尺寸：', image_file.size
        width_old, height_old = image_file.size
        width_new, height_new = image_file.size
        if height_old > height_limit:
            print __name__, '按高压缩'
            height_new = height_limit
            width_new = int((float(height_limit) / height_old) * width_old)
        save_image = image_file.resize((width_new, height_new), Image.ANTIALIAS)

        # if image_type == 'image/jpeg':
        #     print __name__, '图片是jpg，压缩质量：', quality
        #     save_image.save(save_path, quality=quality)
        # else:
        #     print __name__, '图片不是jpg'
        #     save_image.save(save_path)
        save_image.save(save_path, format='jpeg', quality=quality)

        result_size = os.path.getsize(save_path)
        print __name__, '最终图片：', save_image.size, result_size / 1024.0
        return result_size
    except Exception as e:
        print __name__, '对图片进行尺寸压缩出错：', e
        return 0


def compress_image_file_by_width_limit(image_file, image_type, save_path, width_limit, quality):
    try:
        print __name__, '宽限制：', width_limit
        print __name__, '图片尺寸：', image_file.size
        width_old, height_old = image_file.size
        width_new, height_new = image_file.size
        if width_old > width_limit:
            print __name__, '按宽压缩'
            width_new = width_limit
            height_new = int((float(width_limit) / width_old) * height_old)
        save_image = image_file.resize((width_new, height_new), Image.ANTIALIAS)

        # if image_type == 'image/jpeg':
        #     print __name__, '图片是jpg，压缩质量：', quality
        #     save_image.save(save_path, quality=quality)
        # else:
        #     print __name__, '图片不是jpg'
        #     save_image.save(save_path)
        save_image.save(save_path, format='jpeg', quality=quality)

        result_size = os.path.getsize(save_path)
        print __name__, '最终图片：', save_image.size, result_size / 1024.0
        return result_size
    except Exception as e:
        print __name__, '对图片进行尺寸压缩出错：', e
        return 0


def compress_image_file_by_dimension_limit(image_file, image_type, save_path, width_limit, height_limit, quality):
    """
    对图片进行尺寸压缩， 如果图片为jpg，按制定质量保存
    :param quality: jpg保存质量
    :param image_type: 图片类型，对于jpg格式的，保存质量
    :param image_file: 图片文件对象，非路径
    :param save_path:   图片保存路径
    :param width_limit:     宽限制
    :param height_limit:    高限制
    :return:
    """
    try:
        print __name__, '宽高限制：', width_limit, height_limit
        print __name__, '图片尺寸：', image_file.size
        width_old, height_old = image_file.size
        width_new, height_new = image_file.size

        save_image = image_file
        # 压缩宽度
        if width_old > width_limit:
            width_new = width_limit
            height_new = int((float(width_limit) / width_old) * height_old)
            save_image = image_file.resize((width_new, height_new), Image.ANTIALIAS)

        print __name__, 'height_new:', height_new, 'width_new:', width_new
        # 压缩高度
        if height_new > height_limit:
            height_new_new = height_limit
            width_new_new = int((float(height_limit) / height_new) * width_new)
            save_image = save_image.resize((width_new_new, height_new_new), Image.ANTIALIAS)

        # if image_type == 'image/jpeg':
        #     print __name__, '图片是jpg，压缩质量：', quality
        #     save_image.save(save_path, quality=quality)
        # else:
        #     print __name__, '图片不是jpg'
        #     save_image.save(save_path)
        save_image.save(save_path, format='jpeg', quality=quality)

        result_size = os.path.getsize(save_path)
        print __name__, '最终图片：', save_image.size, result_size / 1024.0
        return result_size
    except Exception as e:
        print __name__, '对图片进行尺寸压缩出错：', e
        return 0


def compress_image_file_by_dimension_limit_logo(image_file, image_type, save_path, width_limit, height_limit, quality):
    """
    对图片进行尺寸压缩， 如果图片为jpg，按制定质量保存
    :param quality: jpg保存质量
    :param image_type: 图片类型，对于jpg格式的，保存质量
    :param image_file: 图片文件对象，非路径
    :param save_path:   图片保存路径
    :param width_limit:     宽限制
    :param height_limit:    高限制
    :return:
    """
    try:
        print __name__, '宽高限制：', width_limit, height_limit
        print __name__, '图片尺寸：', image_file.size
        width_old, height_old = image_file.size
        width_new, height_new = image_file.size

        save_image = image_file
        # 压缩宽度
        if width_old > width_limit:
            width_new = width_limit
            height_new = int((float(width_limit) / width_old) * height_old)
            save_image = image_file.resize((width_new, height_new), Image.ANTIALIAS)

        print __name__, 'height_new:', height_new, 'width_new:', width_new
        # 压缩高度
        if height_new > height_limit:
            height_new_new = height_limit
            width_new_new = int((float(height_limit) / height_new) * width_new)
            save_image = save_image.resize((width_new_new, height_new_new), Image.ANTIALIAS)

        if image_type == 'image/jpeg':
            print __name__, '图片是jpg，压缩质量：', quality
            save_image.save(save_path, quality=quality)
        else:
            print __name__, '图片不是jpg'
            save_image.save(save_path)

        result_size = os.path.getsize(save_path)
        print __name__, '最终图片：', save_image.size, result_size / 1024.0
        return result_size
    except Exception as e:
        print __name__, '对图片进行尺寸压缩出错：', e
        return 0

def compress_image_file_to_size_limit(image_file, image_type, save_path, size_origin, size_limit, quality):
    """
    将图片weight压缩到指定大小内
    :param image_file:
    :param image_type:
    :param save_path:
    :param size_origin:
    :param size_limit:
    :param quality:
    :return:
    """
    try:
        size_limit *= 1024
        size_tmp = size_origin
        q = 100
        while size_tmp > size_limit and q > quality and image_type == 'image/jpeg':
            out_ = image_file.resize(image_file.size, Image.ANTIALIAS)
            out_.save(save_path, quality=q)
            size_tmp = os.path.getsize(save_path)
            q -= 5
        if q == 100:
            image_file.save(save_path)
        return os.path.getsize(save_path)
    except Exception as e:
        print __name__, '对图片进行尺寸压缩出错：', e
        return 0
