# -*- coding:utf-8 -*- 
# --------------------
# Author:   mofei
# Description:
# 1、chart 中的 choose_time 字段为时间插件格式
# 2、chart 中的 page 字段为分页插件
# 3、chart 中的 search 字段为搜索插件
# ----------------

import datetime

# 表格返回给前端数据格式list中，一个字典对应一个表
chart = [
    {
        # 图表类型:table 表格，pie 饼状图， line 线状图， column 柱状图
        'chart_type': 'table',
        # 图表唯一标识，更新用
        'chart_id': 1,
        # 图表名字
        'chart_title': '载客汽车百吨公里燃料消耗量',
        # 时间插件，不用 choose_time: False
        'choose_time': {
            'end_date': datetime.datetime.now().strftime('%Y-%m'),  # 结束日期
            'days': 365,  # 和结束日期逆推算开始日期
            'date_type': 'YYYY-MM',  # 时间格式： 'YYYY-MM' 2017-08, 'YYYY' 2017
            'view_type': False,  # 'year' 年， 'month' 月， 'quarterly' 季度， False 不用
            'is_single': True,  # 单选
        },
        # 分页插件: 不用就不写，或 'page': False
        'page': {
            'page_current': 1,  # 当前显示页
            'page_total': 5,  # 总页数
        },
        # 搜索插件：不用不写，或 'search': False
        'search': True,
        # 图表的具体数据
        'data': {
            'title': ['车牌号', '燃油类型', '百公里能耗'],
            'data': [
                ['贵A2388', '汽油', 100],
                ['贵A2388', '汽油', 100],
                ['贵A2388', '汽油', 100],
                ['贵A2388', '汽油', 100],
                ['贵A2388', '汽油', 100],
                ['贵A2388', '汽油', 100],
                ['贵A2388', '汽油', 100],
            ]
        }
    },
]

# 表格数据格式
data_table = {
    # 表格每列的标题
    'title': ['车牌号', '燃油类型', '百公里能耗'],
    # 每个list对应一行
    'data': [
        ['贵A2388', '汽油', 100],
        ['贵A2388', '汽油', 100],
        ['贵A2388', '汽油', 100],
        ['贵A2388', '汽油', 100],
        ['贵A2388', '汽油', 100],
        ['贵A2388', '汽油', 100],
        ['贵A2388', '汽油', 100],
    ]
}
# 线、柱状图数据格式
data_line_column = {
    # x轴坐标
    'legend': ['2016', '2017', '2018'],
    # 一个字典一条线
    'data': [
        {'name': '油耗趋势', 'data': [3223, 23435, 23435]},
        {'name': '排放趋势', 'data': [13223, 123435, 123435]},
    ]
}
# 饼状图数据格式
data_pie = {
    'type': 'pie',
    'name': "占比",
    'data': [
        ['柴油(200)', 200],
        ['汽油(300)', 300],
        ['天然气(400)', 400],
        ['甲醇(500)', 500],
    ]
}


# 驾培
{
    "status": 1,
    "msg": "success",
    "data": {
        "all_students": 0,  # 学员数
        "maintenance_over_time": 5397,  # 保养时间超一年
        "all_proprietor": 68,  # 所有业户
        "insure_expire": 2571,  # 保险到期数
        "all_expire": 26,  # 经营权限到期
        "all_vehicle": 6250  # 所有车辆数
    }
}

# 出租
{
    "status": 1,
    "msg": "success",
    "data": {
        "all_passenger": 0,  # 乘客数
        "maintenance_over_time": 5397,  # 保养时间超一年
        "all_proprietor": 68,  # 所有业户
        "insure_expire": 2571,  # 保险到期数
        "all_expire": 26,  # 经营权限到期
        "all_vehicle": 6250  # 所有车辆数
    }
}
