# -*- coding:utf-8 -*- 
# --------------------
# Author:		gxm1015@qq.com
# Description:	一些公用常量
# --------------------
# 车辆类型
VEHICLE_TYPE = {
    1: "freight_vehicle",  # 货运（111805）
    2: "danger_freight_vehicle",  # 危货（1018）
    3: "taxi",  # 出租车（8984）
    4: "passenger_vehicle",  # 客运车, 班线车（2418）
    5: "tourist_vehicle",  # 旅游班车（1415）
    6: "bus",  # 公交车（3131）
    7: "training_vehicle",  # 驾培车（6204）
    8: "net_about_car",  # 网约车（2）
    101: "law_people",  # 执法人员（自编）
    102: "law_vehicle",  # 执法车辆（自编）
    103: "law_unit",  # 执法单位（自编）
    104: 'passenger_station',  # 客运场站（自编）
}
VEHICLE_TYPE_CN = {
    1: u"货运车辆",
    2: u"危货车辆",
    3: u"出租车",
    4: u"客运车辆",
    5: u"旅游包车",
    7: u"驾培车辆",
    8: u"网约车",
    101: u"执法人员",
    102: u"执法车辆",
    103: u"执法单位",
    104: u"客运场站"
}
VEHICLE_TYPE_REVERSE = {
    "freight_vehicle": 1,  # 货运
    "danger_freight_vehicle": 2,  # 危货
    "taxi": 3,  # 出租车
    "passenger_vehicle": 4,  # 客运车, 班线车
    "tourist_vehicle": 5,  # 旅游班车
    "bus": 6,  # 公交车
    "training_vehicle": 7,  # 驾培车
    "net_about_car": 8,  # 网约车
    "law_people": 101,  # 执法人员
    "law_vehicle": 102,  # 执法车辆
    "law_unit": 103,  # 执法单位
    "passenger_station": 104,  # 客运场站
}
VEHICLE_NAME_EN_TO_CN = {
    "freight_vehicle": u'普通货运车辆',
    "danger_freight_vehicle": u'危险品运输车辆',
    "taxi": u'出租车',
    "passenger_vehicle": u'客运车辆',
    "tourist_vehicle": u'旅游包车',
    "bus": u'公交车',
    "training_vehicle": u'教练车',
    'net_about_car': u'网约车',
    'law_people': u'执法人员',
    'law_unit': u'执法单位',
    'passenger_station': u'客运场站'

}

# 业户类型
PROPRIETOR_TYPE = {
    1: 'passenger_proprietor',
    2: 'normal_freight_proprietor',
    3: 'danger_freight_proprietor',
    4: 'bus_proprietor',
    5: 'taxi_proprietor',
    6: 'training_proprietor',
    7: 'fix_proprietor',
    8: 'monitor_proprietor',
    9: 'passenger_station_proprietor',
    10: 'freight_station_proprietor',
    11: 'handling_proprietor'
}
PROPRIETOR_TYPE_REVERSE = {
    'passenger_proprietor': 1,
    'normal_freight_proprietor': 2,
    'danger_freight_proprietor': 3,
    'bus_proprietor': 4,
    'taxi_proprietor': 5,
    'training_proprietor': 6,
    'fix_proprietor': 7,
    'monitor_proprietor': 8,
    'passenger_station_proprietor': 9,
    'freight_station_proprietor': 10,
    'handling_proprietor': 11
}
PROPRIETOR_NAME_EN_TO_CN = {
    'passenger_proprietor': u'客运公司',
    'normal_freight_proprietor': u'普通货运公司',
    'danger_freight_proprietor': u'危险品运输公司',
    'bus_proprietor': u'公交公司',
    'taxi_proprietor': u'出租车公司',
    'training_proprietor': u'驾校',
    'fix_proprietor': u'维修站',
    'monitor_proprietor': u'监测站',
    'passenger_station_proprietor': u'客运站',
    'freight_station_proprietor': u'货运站',
    'handling_proprietor': u'搬运装卸'
}

# 从业人员
CAREER_TYPE = {
    1: 'coach',
    2: 'driver',
    3: 'fix',
    4: 'handling',
    5: 'escorts'
}
CAREER_TYPE_REVERSE = {
    'coach': 1,
    'driver': 2,
    'fix': 3,
    'handling': 4,
    'escorts': 5
}
CAREER_NAME_EN_TO_CN = {
    'coach': u'教练员',
    'driver': u'驾驶员',
    'fix': u'维修员',
    'handling': u'搬运装卸',
    'escorts': u'押运员'
}
CAREER_SPECIAL_LIST_ID = {
    1: (26, 27, 28, 29, 30, 31),
    2: (1, 2, 3, 7, 11, 15, 32, 43, 44, 47),
    3: (19, 20, 21, 22, 23, 24, 25, 41, 42),
    4: (4, 8, 12, 16),
    5: (5, 9, 13, 17)
}

# 风险等级(sep)
WARNING_LEVEL_ID_TO_CN = {
    1: u'风险等级一',
    2: u'风险等级二',
    3: u'风险等级三',
    4: u'风险等级四',
}

# 事件状态（sep)
EVENT_STATE_CODE_TO_CN = {
    1: u'未开始',
    2: u'进行中',
    3: u'已完成',
}


# CACHE KEY
LCIC_CACHE_KEY = 'lcic_cache:{0}'

# CACHE EXPIRE
MINUTE = 60
HALF_HOUR = 60 * 30
HOUR = 60 * 60
HALF_DAY = 60 * 60 * 12
DAY = 60 * 60 * 24
CACHE_DATA_TIMEOUT = 60 * 5  # 零时、半固定缓存的过期时间，秒；过期后刷新缓存
CACHE_DATA_LIFE = 10   # 零时缓存的生命周期，天；过期删除
# 车辆当前位置过期时间, 过期没有更新将从地图上移除
VEHICLE_EXPIRE_SECOND = 60 * 10

# 出租车聚集事件
LCIC_MAIN_TAXI_FOCUS_ZONE_EXPIRE_TIME = 60 * 5  # 过期时间，分钟
LCIC_MAIN_TAXI_FOCUS_ZONE_ALARM_TIME = 10  # 预警时间，分钟
LCIC_MAIN_TAXI_FOCUS_CHECK_TIME = 60 * 30  # 线程多久检查一次，秒钟

# 行政执法常量
LAW_HOT_SPOT_DAYS = 600  # 执法热点查询最近多少天的数据
LAW_HOT_SPOT_ITEMS = 20  # 执法热点显示多少条数据
LAW_ENFORCEMENT_NUM_MONTHS = 18  # 执法数量统计最近多少个月的数据
LAW_ANALYSIS_MONTHS = 10  # 执法分析统计多少个月的数据
LAW_ROUTE_STATISTIC_YEAR = 5  # 客运班次统计几年的数据

# 数据管理平台
DATA_MANAGE_ITEM_PER_PAGE = 20  # 每页显示多少条

# 历史轨迹去重
DISTANCE_INTERVAL = 10  # m, 两点距离为多大认为是同一个点
TIME_INTERVAL = 0  # s, 两点时间差为多少认为是同一个点
MAX_VELOCITY = 56  # m/s, 对应时速 200km/h

# 调度自动结束时间
DISPATCH_AUTO_FINISH = 6  # 小时，从创建开始，多久自动结束
DISPATCH_AUTO_FINISH_CHECK = 30  # 秒, 多久检查一次

# 推送程序多久推送一次数据
PUBLISH_INTERVAL = 3  # 秒

