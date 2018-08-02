# -*- coding:utf-8 -*- 
# --------------------
# Author:		Ken
# Description:	地理信息工具库
# --------------------

from math import radians, cos, sin, asin, sqrt


# 电子围栏，判断是否在多边形内
def is_pt_in_poly(Alon, Alat, Apoints):
    """
    :param Alon: lng
    :param Alat: lat
    :param Apoints: [{'lng':lng, 'lat':lat},{'lng':lng, 'lat':lat},...]
    :return:
    """
    # TODO: Change Apoints format to [(lng, lat),(lng, lat),(lng, lat)...]
    iSum = 0
    if not Apoints or len(Apoints) < 3:
        return False
    for index, point in enumerate(Apoints):
        dLon1 = point['lng']
        dLat1 = point['lat']
        if index == len(Apoints) - 1:
            dLon2 = Apoints[0]['lng']
            dLat2 = Apoints[0]['lat']
        else:
            dLon2 = Apoints[index + 1]['lng']
            dLat2 = Apoints[index + 1]['lat']
        if (Alat >= dLat1 and Alat < dLat2) or (Alat >= dLat2 and Alat < dLat1):
            if abs(dLat1 - dLat2) > 0:
                dLon = dLon1 - ((dLon1 - dLon2) * (dLat1 - Alat)) / (dLat1 - dLat2)
                if dLon < Alon:
                    iSum += 1
    if iSum % 2 != 0:
        return True
    return False


# 计算两个经纬度间的距离
def get_distance(lon1, lat1, lon2, lat2):  # 经度1，纬度1，经度2，纬度2 （十进制度数）
    # 将十进制度数转化为弧度
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # haversine公式
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    r = 6371  # 地球平均半径，单位为公里
    return c * r * 1000


def distance(record1, record2):
    """
    两点间距离
    :param record1:
    :param record2:
    :return:
    """
    return get_distance(record1['lng'], record1['lat'], record2['lng'], record2['lat'])


def time_interval(record1, record2):
    """
    两点间的时间间隔
    :param record1: 第一个记录点
    :param record2: 第二个记录点
    :return: 两个记录点间的时间差的秒数
    """

    if record1['time'] > record2['time']:
        result = record1['time'] - record2['time']
    else:
        result = record2['time'] - record1['time']
    return result.days * 24 * 60 * 60 + result.seconds


def velocity(record1, record2):
    """
    两点间的平均速度
    :param record1:
    :param record2:
    :return:
    """
    interval_time = time_interval(record2, record1)
    interval_distance = get_distance(record1['lng'], record1['lat'], record2['lng'], record2['lat'])
    if interval_time > 0:
        return interval_distance / interval_time
    else:
        return None


def acceleration(record1, record2, record3):
    """
    加速度
    :param record1:
    :param record2:
    :param record3:
    :return:
    """
    time_used = (time_interval(record1, record3))
    v1 = velocity(record1, record2)
    v2 = velocity(record2, record3)
    if time_used > 0:
        return abs(v1 - v2) / time_used
    else:
        return 0
