# -*- coding:utf-8 -*- 
# --------------------
# Author:       SDN
# Description:	所有模块公用的基
# Time:         17/06/08
# --------------------
from modules.common.model.dbManager import psdb, rsdb, psdb_for_update_cache
from utils.coordTransform import wgs84_to_map_coordinate, map_coordinate_to_wgs84


class BaseModel(object):
    def __init__(self):
        # 用于刷新缓存（仅query）
        self.server_for_update_cache = psdb_for_update_cache

        self.server = psdb
        self.redis_db = rsdb

    def wgs84_to_map_coordinate(self, pt_list, coordinate_type=None):
        """
        数据库中的位置用的wgs84，根据地图，转换成相应的格式;
        :param coordinate_type: None 默认， 'bd09' 百度，'gcj02' 火星
        :type pt_list: [(lng, lat),...]
        :return: [(lng, lat),...]
        """
        return wgs84_to_map_coordinate(pt_list, coordinate_type)

    def map_coordinate_to_wgs84(self, pt_list, coordinate_type=None):
        """
        地图坐标转换为wgs84
        :param pt_list:
        :param coordinate_type: None 默认， 'bd09' 百度，'gcj02' 火星
        :return:
        """
        return map_coordinate_to_wgs84(pt_list, coordinate_type)

    def get_month_last_day(self, year_month):
        """
        获取一个月的最后一天
        :param year_month:
        :return: 这个月最后天的日子，str
        """
        year, month = year_month.split('-')
        if month in ['1', '3', '5', '7', '8', '01', '03', '05', '07', '08', '10', '12']:
            return '31'
        elif month in ['4', '6', '9', '04', '06', '09', '11']:
            return '30'
        else:
            year = int(year)
            if year % 4 == 0 and year % 100 != 0 or year % 400 == 0:
                return '29'
            else:
                return '28'

    def get_year(self, year_month):
        """

        :param year_month: '2015-07'
        :return:
        """
        return year_month.split('-')[0]

    def get_year_month(self, year_month):
        """

        :param year_month: '2015-07'
        :return:
        """
        return year_month.split('-')[0: 2]

    def sum_list(self, list_value):
        """
        数字型list中的元素的和
        :param list_value:
        :return:
        """
        if list_value:
            a = 0
            for item in list_value:
                a += item
            return a
        else:
            return 0

    def get_month_x_legend(self, year_month_start, year_month_end):
        """
        获取 x 轴的名字, 按月
        :param year_month_start:
        :param year_month_end:
        :return:['2017-01', '2017-02', ...]
        """

        def get_legend_x_month(y, month_s, month_e):
            """

            :param y:年
            :param month_s: 开始的月
            :param month_e: 结束月
            :return:
            """
            legend_x_x = []
            for mon in range(int(month_s), int(month_e) + 1):
                if mon >= 10:
                    legend_x_x.append(str(y) + '-' + str(mon))
                else:
                    legend_x_x.append(str(y) + '-0' + str(mon))
            return legend_x_x

        year_start, month_start = self.get_year_month(year_month_start)
        year_end, month_end = self.get_year_month(year_month_end)
        if year_start == year_end:
            return get_legend_x_month(year_start, month_start, month_end)
        else:
            first_year = get_legend_x_month(year_start, month_start, 12)
            end_year = get_legend_x_month(year_end, 1, int(month_end))
            interval_year = []
            if int(year_end) - int(year_start) > 1:
                for yye in range(int(year_start) + 1, int(year_end)):
                    for i in range(1, 13):
                        if i < 10:
                            interval_year.append(str(yye) + '-0' + str(i))
                        else:
                            interval_year.append(str(yye) + '-' + str(i))

            return first_year + interval_year + end_year

    def get_year_x_legend(self, year_month_start, year_month_end):
        """
        获取 x 轴的名字, 按年
        :param year_month_start:
        :param year_month_end:
        :return: ['2015', 2016', ...]
        """
        year_x_legend = []
        year_start = self.get_year(year_month_start)
        year_end = self.get_year(year_month_end)
        for yee in range(int(year_start), int(year_end) + 1):
            year_x_legend.append(str(yee))
        return year_x_legend

    def get_quarterly_x_legend(self, year_month_start, year_month_end):
        """
        获取 x 轴的名字, 按季度
        :param year_month_start:
        :param year_month_end:
        :return: ['2015-1', '2015-2', ...]
        """
        year_start, month_start = self.get_year_month(year_month_start)
        year_end, month_end = self.get_year_month(year_month_end)

        # 起
        if 1 <= int(month_start) <= 3:
            quarterly_start = 1
        elif 4 <= int(month_start) <= 6:
            quarterly_start = 2
        elif 7 <= int(month_start) <= 9:
            quarterly_start = 3
        else:
            quarterly_start = 4

        # 止
        if 1 <= int(month_end) <= 3:
            quarterly_end = 1
        elif 4 <= int(month_end) <= 6:
            quarterly_end = 2
        elif 7 <= int(month_end) <= 9:
            quarterly_end = 3
        else:
            quarterly_end = 4

        if year_start == year_end:
            return [year_start + '-' + str(quar) for quar in range(quarterly_start, quarterly_end + 1)]
        else:
            quarterly_list_start_year = [year_start + '-' + str(quar) for quar in range(quarterly_start, 5)]
            quarterly_list_interval = []
            quarterly_list_end_year = [year_end + '-' + str(quar) for quar in range(1, quarterly_end + 1)]
            if int(year_end) - int(year_start) > 1:
                for yee in range(int(year_start) + 1, int(year_end)):
                    quarterly_list_interval.append(str(yee) + '-1')
                    quarterly_list_interval.append(str(yee) + '-2')
                    quarterly_list_interval.append(str(yee) + '-3')
                    quarterly_list_interval.append(str(yee) + '-4')
            return quarterly_list_start_year + quarterly_list_interval + quarterly_list_end_year

    def get_x_legend(self, view_type, year_month_start, year_month_end):
        if view_type == 'year':
            return self.get_year_x_legend(year_month_start, year_month_end)
        elif view_type == 'quarterly':
            return self.get_quarterly_x_legend(year_month_start, year_month_end)
        else:
            return self.get_month_x_legend(year_month_start, year_month_end)

    def only_year_month_date(self, date_str, is_start=False):
        """
        获取年月格式的时间
        :param is_start:
        :param date_str:
        :return:
        """
        date_split = date_str.split('-')
        if len(date_split) >= 2:
            return date_split[0] + '-' + date_split[1]
        else:
            if is_start:
                return date_str + '-1'
            else:
                return date_str + '-12'
