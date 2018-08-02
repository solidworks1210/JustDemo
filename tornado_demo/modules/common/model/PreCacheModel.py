# -*- coding:utf-8 -*- 
# --------------------
# Author:   mofei
# Description:	程序在运行过程中产生的缓存，但需要在程序启动时预先缓存
# ----------------
from tornado.log import app_log

from conf.redis_key import LCIC_MAIN_CLIENT_STATE_KEY, LCIC_MAIN_VEHICLE_BASIC_INFO_KEY
from modules.analysis.model.DataManageModel import data_flow_model, data_manage_model
from modules.analysis.model.LawModel import law_model as layer_law_model
from modules.analysis.model.PassengerStationModel import passenger_station_model as layer_passenger_station_model
from modules.analysis.model.StatisticDangerFreightVehicleModel import statistic_danger_freight_model
from modules.analysis.model.StatisticLawModel import statistic_law_model
from modules.analysis.model.StatisticPassengerVehicleModel import statistic_passenger_vehicle_model
from modules.analysis.model.StatisticTaxiModel import statistic_taxi_model
from modules.analysis.model.StatisticTouristVehicleModel import statistic_tourist_vehicle_model
from modules.analysis.model.StatisticTrainingVehicleModel import statistic_training_vehicle_model
from modules.common.model.BaseModel import BaseModel


class PreCacheModel(BaseModel):
    def clean_cache(self):
        """
        清除缓存
        :return:
        """
        # 清除基本信息
        self.redis_db.delete(LCIC_MAIN_VEHICLE_BASIC_INFO_KEY)

    def pre_cache(self):
        """
        预缓存
        :return:
        """
        # 清除客户端状态
        self.redis_db.delete(LCIC_MAIN_CLIENT_STATE_KEY)
        # 为了预缓存
        can_del = False
        if not self.redis_db.exists(LCIC_MAIN_VEHICLE_BASIC_INFO_KEY):
            self.redis_db.hset(LCIC_MAIN_VEHICLE_BASIC_INFO_KEY, 'lcic', 'lcic')
            can_del = True
        # 缓存数据
        app_log.info('---> pre_cache start <---')
        # analysis
        layer_law_model.pre_cache()
        layer_passenger_station_model.pre_cache()
        statistic_law_model.pre_cache()
        statistic_passenger_vehicle_model.pre_cache()
        statistic_danger_freight_model.pre_cache()
        statistic_tourist_vehicle_model.pre_cache()
        statistic_taxi_model.pre_cache()
        statistic_training_vehicle_model.pre_cache()

        data_flow_model.pre_cache()  # 数据流图数据
        data_manage_model.pre_cache()  # 数据管理

        # cap

        # esp

        # sep

        if can_del:
            self.redis_db.delete(LCIC_MAIN_VEHICLE_BASIC_INFO_KEY)
        app_log.info('---> pre_cache finish <---')

pre_cache_model = PreCacheModel()
