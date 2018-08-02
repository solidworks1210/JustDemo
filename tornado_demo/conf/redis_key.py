# -*- coding:utf-8 -*- 
# --------------------
# Author:   mofei
# Description:	redis 使用的各种key（部分，原始逐步迁移过来）
# ----------------

# ----------------------- 队列(主、同步都在用)
LCIC_PUBLIC_VEHICLE_GPS_QUEUE_KEY = "lcic_public_vehicle_gps_queue:key"  # hash方式的队列

# ------------------------ 车辆基本信息缓存key
LCIC_MAIN_VEHICLE_BASIC_INFO_KEY = "lcic_main_vehicle_basic_info:key"  # 所有车辆详情信息缓存（两客一危、出租车、驾培，同一张表，合在一起比较好）

# ----------------------- 车辆当前位置信息缓存key
LCIC_MAIN_VEHICLE_CURRENT_GPS_INFO_KEY = "lcic_main_vehicle_current_gps_info:key"  # 包含车辆类型的GPS信息缓存KEY(车辆最近一次的定位信息)

# ----------------------- 客户端信息缓存（运行时产生的缓存）
LCIC_MAIN_CLIENT_STATE_KEY = "lcic_main_client_state_info:key"  # 客户端状态信息KEY

# ----------------------- 出租车聚集缓存
LCIC_MAIN_TAXI_FOCUS_ZONE_VEHICLE_KEY = 'lcic_main_taxi_focus_zone_vehicles:key'  # 围栏中车缓存（运行缓存）

# ----------------------- 各类半固定信息用到的缓存（同一个hash，通过field区分，value中包含最近一次查数据库的时间）（运行时产生的缓存）
LCIC_MAIN_SEMI_FIXED_INFO_KEY = 'lcic_main_semi_fixed_info:key'

# ----------------------- 零时缓存数据, 过期删除(每个field除了时间字段，还要加入日期字段)
LCIC_MAIN_TEMP_FIXED_INFO_KEY = 'lcic_main_temp_fixed_info:key'

