# -*- coding:utf-8 -*- 
# --------------------
# Author:		gxm1015@qq.com
# Description:	Vehicle info message real time push to client.
# --------------------
import threading
import time

from tornado.concurrent import app_log
from tornado.escape import json_decode

from conf.constant import PUBLISH_INTERVAL
from modules.analysis.model.PublishCtlModel import publish_ctrl_model, vehicle_gps_queue_instance
from modules.analysis.model.PublishLocationUpdateModel import client_state_cache_instance
from .PublishLocationUpdateHandler import LocationRealTimeUpdateHandler


# 系统启动通过就启动推送线程
def start_publish_thread():
    """
    思路：一次拿一批数据，将所有数据处理完后，打包批量推送
    :return:
    """

    def start_push():
        app_log.warn('---> Publish thread started <---')
        # 最近的一次获取的数据的条数，超过一定值，下次取数据要清空队列
        last_data_len = 0
        # 上一次操作开始的时间
        last_action_start_time = 0
        while True:
            try:
                time_start = time.time()  # 每批数据开始处理的时间
                data_to_publish = {}  # {‘session_id’: {'vehicle_card': data, ...}, ...}
                counter = 0  # 达到多少条就推送
                counter_push = 0  # 要推送的条数
                # 取数据
                if last_data_len > 20000:
                    # 要清理队列
                    dict_data = vehicle_gps_queue_instance.get_publish_data_with_clear()
                    app_log.warn('Clear queue ------------ ')
                else:
                    # 不清理队列
                    dict_data = vehicle_gps_queue_instance.get_publish_data()
                # 判断数据是否为空
                if not dict_data:
                    last_data_len = 0
                    last_action_start_time = time_start
                    time.sleep(PUBLISH_INTERVAL)
                    continue
                # 本次拿取数据的条数
                last_data_len = len(dict_data)
                # 计时，从缓存中获取数据所花费的时间
                time_get = time.time() - time_start
                # 处理要推送的数据
                time_push_start = time.time()
                for msg_json in dict_data.itervalues():
                    try:
                        msg_dict = json_decode(msg_json)
                        # 筛选过时数据
                        if msg_dict['insert_time'] >= last_action_start_time:
                            # 获取该条数据要推送的客户端
                            session_id_list = client_state_cache_instance.get_need_push_session_id_list(msg_dict['type'])
                            # 需要推送
                            if session_id_list:
                                for session_id in session_id_list:
                                    msg_dict_update = publish_ctrl_model.update_vehicle_current_gps_cache(msg_dict)
                                    # 客户端是否缓存了
                                    temp = data_to_publish.get(session_id, None)
                                    if temp:
                                        temp[msg_dict_update['data']['vehicle_card']] = msg_dict_update
                                    else:
                                        data_to_publish[session_id] = {
                                            msg_dict_update['data']['vehicle_card']: msg_dict_update,
                                        }
                                counter += 1
                                counter_push += 1

                                # 超量推送
                                if counter >= 1500:
                                    LocationRealTimeUpdateHandler.send_message_package(data_to_publish)
                                    counter = 0
                                    data_to_publish = {}
                                    # todo: 这儿需要休息不？？？？
                                    # time.sleep(1)
                            # 不需推送
                            else:
                                # 该条记录无推送客户端，更新缓存中的位置信息
                                publish_ctrl_model.update_vehicle_current_gps_cache(msg_dict)
                    except Exception as e:
                        app_log.error(e)
                        import traceback
                        traceback.print_exc()
                # 向前端推送
                if data_to_publish:
                    LocationRealTimeUpdateHandler.send_message_package(data_to_publish)
                # 时间管理
                total_time_coast = time.time() - time_start
                if total_time_coast >= PUBLISH_INTERVAL:
                    app_log.info('All data get: {0}, used time: {1} <---> All data push: {2}, used time: {3} <---> Total time coast: {4}'
                                 .format(last_data_len, time_get, counter_push, time.time() - time_push_start, total_time_coast, ))
                    last_action_start_time = time_start
                    continue
                else:
                    app_log.info('All data get: {0}, used time: {1} <---> All data push: {2}, used time: {3} <---> Total time coast: {4}'
                                 .format(last_data_len, time_get, counter_push, time.time() - time_push_start, total_time_coast, ))
                    time.sleep(PUBLISH_INTERVAL - total_time_coast)
                    last_action_start_time = time_start
            except Exception as e:
                app_log.error(e)
                import traceback
                traceback.print_exc()

    # 不用线程池， 减小系统开销
    publish_thread = threading.Thread(target=start_push)
    publish_thread.setDaemon(True)
    publish_thread.start()
