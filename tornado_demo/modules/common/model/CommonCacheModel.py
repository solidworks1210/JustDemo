# -*- coding:utf-8 -*- 
# --------------------
# Author:
# Description:	
# --------------------
import datetime
import threading
import time
from functools import wraps

from concurrent.futures import ThreadPoolExecutor
from tornado.escape import json_decode, json_encode
from tornado.log import app_log

from conf.constant import CACHE_DATA_TIMEOUT, CACHE_DATA_LIFE
from conf.redis_key import LCIC_MAIN_SEMI_FIXED_INFO_KEY, LCIC_MAIN_TEMP_FIXED_INFO_KEY, LCIC_MAIN_VEHICLE_BASIC_INFO_KEY
from .dbManager import rsdb

_thread_pool = ThreadPoolExecutor(6)
_date_today = datetime.datetime.now().strftime('%Y-%m-%d')


def can_action(func):
    @wraps(func)
    def wrapper(*args, **kw):
        if rsdb.exists(LCIC_MAIN_VEHICLE_BASIC_INFO_KEY):
            return func(*args, **kw)
        else:
            return None

    return wrapper


def generate_field(field, obj, func, args, kwargs):
    """
    生成hash的field
    :param kwargs:
    :param args:
    :param func:
    :param obj:
    :param field:
    :return:
    """

    def to_str(ag):
        if not (isinstance(ag, type(u'')) or isinstance(ag, type(''))):
            ag = str(ag)
        if isinstance(ag, type(u'')):
            ag = ag.encode('utf-8')
        return ag

    if field is None:
        _field = str(hash(to_str(obj.__class__) + to_str(func.__name__) + to_str(args) + to_str(kwargs)))
    else:
        _field = field
    return _field


def first_use_cached_data(timeout=CACHE_DATA_TIMEOUT, key=LCIC_MAIN_SEMI_FIXED_INFO_KEY, field=None, immediately_refresh=False):
    """
    0、仅用于装饰类方法
    1、该装饰器修饰的方法，会优先使用缓存中的数据，缓存中无数据才调用修饰的方法，并缓存结果
    2、只要缓存有数据，不管是否过期，都返回缓存的数据，并根据是否过期在后台使用线程更新缓存
    3、timeout 为 0，数据不过期，不会更新数据
    4、使用hash， field对应缓存的值
    5、不传入field，自动生成field: 类名+方法名+参数 字符串的 hash值
    6、装饰器修饰的方法包含 'immediately_refresh' 在键值对参数时，要立即更新
    :param immediately_refresh: True 返回缓存数据，立即后台更新，忽略timeout
    :param timeout: 重新从数据库获取数据的时间间隔
    :param key: hash key
    :param field: hash f
    :return:
    """

    def cache_to_redis(fun):
        @wraps(fun)
        def decorators(self, *args, **kwargs):
            # 生成_field
            _field = generate_field(field, self, fun, args, kwargs)

            # 后台缓存数据的方法（线程）
            def cache_data_in_background_thread():
                """
                数据过期，返回旧的数据，在后台更新缓存
                :return:
                """

                def _start():
                    app_log.debug('---> refresh cache: {0}'.format(fun.__name__))
                    _data_from_db = fun(self, *args, **kwargs)
                    _data_to_cache = {
                        'data': _data_from_db,
                        'last_query_time': str(time.time())
                    }
                    rsdb.hset(
                        key,
                        _field,
                        json_encode(_data_to_cache)
                    )

                _thread_pool.submit(_start)

            # 从缓存拿取数据
            data_from_cache = rsdb.hget(key, _field)
            # 分析数据
            if data_from_cache:
                # 数据存在，更具过期时间进行操作
                data_dict = json_decode(data_from_cache)
                # 立即刷新
                if immediately_refresh is True:
                    # 启动后台更新线程
                    cache_data_in_background_thread()
                    # 返回数据
                    return data_dict['data']
                # 不立即刷新
                else:
                    # 不过期
                    if timeout == 0:
                        return data_dict['data']
                    # 要过期
                    else:
                        last_query_time = float(data_dict['last_query_time'])
                        now_time = time.time()
                        if now_time - last_query_time > timeout:
                            # 数据过期，返回旧数据，更新缓存中的时间，以防止多次启动线程；启动线程，更新缓存
                            data_to_cache = {
                                'data': data_dict['data'],
                                'last_query_time': str(time.time())
                            }
                            rsdb.hset(key, _field, json_encode(data_to_cache))
                            # 启动更新线程
                            cache_data_in_background_thread()
                            # 返回数据
                            return data_dict['data']
                        else:
                            return data_dict['data']
            else:
                app_log.debug('<---------> get data from db <---------> {0} <--------->'.format(fun.__name__))
                # 数据不存在，从数库拿取数据，并缓存
                data_from_db = fun(self, *args, **kwargs)
                data_to_cache = {
                    'data': data_from_db,
                    'last_query_time': str(time.time())
                }
                rsdb.hset(key, _field, json_encode(data_to_cache))
                return data_from_db

        return decorators

    return cache_to_redis


def clean_old_cached_data(key=LCIC_MAIN_TEMP_FIXED_INFO_KEY, life=None):
    """
    1、一个线程，用于清除寿命终止的field；
    2、缓存值中包括 last_use_date, life字段
    3、last_use_date 为该缓存最近一次的使用日期：年月日
    4、life 为该缓存的寿命，单位天
    5、可手动调用该方法，清除过期数据（需传入life值）
    :return:
    """
    global _date_today

    def action():
        # print('---> clean old cache data ... <---')
        all_cached_data = rsdb.hgetall(key)
        i = 0
        # 没有给定life值，使用缓存中的life
        if life is None:
            for field, data in all_cached_data.iteritems():
                data_dict = json_decode(data)
                old_date = data_dict['last_use_date']
                now_date = (datetime.datetime.now() - datetime.timedelta(days=int(data_dict['life']))).strftime('%Y-%m-%d')
                if old_date < now_date:
                    rsdb.hdel(key, field)
                    i += 1
        # 按给定的life删
        else:
            for field, data in all_cached_data.iteritems():
                data_dict = json_decode(data)
                old_date = data_dict['last_use_date']
                now_date = (datetime.datetime.now() - datetime.timedelta(days=int(life))).strftime('%Y-%m-%d')
                if old_date < now_date:
                    rsdb.hdel(key, field)
                    i += 1
        # print('---> clean old cache data: {0} <---'.format(i))

    # 自动删除
    if life is None:
        # 给个时间，保证该方法一天仅执行一次
        date_now = datetime.datetime.now().strftime('%Y-%m-%d')
        if date_now != _date_today:
            _date_today = date_now
            action_thread = threading.Thread(target=action, name='deloldcache')
            action_thread.setDaemon(True)
            action_thread.start()
    # 外部删除
    else:
        action_thread = threading.Thread(target=action, name='deloldcache')
        action_thread.setDaemon(True)
        action_thread.start()


def first_use_cached_data_clean_old(timeout=CACHE_DATA_TIMEOUT, life=CACHE_DATA_LIFE, key=LCIC_MAIN_TEMP_FIXED_INFO_KEY, field=None, immediately_refresh=False):
    """
    0、仅用于修饰类方法
    1、装饰类方法, field 为 类 + 方法名 + 参数 的hash字符串
    2、相较于first_use_cached_data， 该装饰器回会根据日期，删除日期过期的数据：比如一个field的
    3、不传入field，自动生成field: 类名+方法名+参数 字符串的 hash值
    4、装饰器修饰的方法包含 'immediately_refresh' 在键值对参数时，要立即更新
    :param field:
    :param life: 缓存的寿命，单位 天
    :param immediately_refresh: True 返回缓存数据，立即后台更新，忽略timeout
    :param timeout: 重新从数据库获取数据的时间间隔, 用于刷新
    :param key: hash key
    :return:
    """

    def cache_to_redis(fun):
        @wraps(fun)
        def decorators(self, *args, **kwargs):

            # 生成_field
            _field = generate_field(field, self, fun, args, kwargs)

            # 后台刷新缓存的方法
            def cache_data_in_background_thread():
                """
                数据过期，返回旧的数据，在后台更新缓存
                :return:
                """

                def _start():
                    # print 'refresh cache: {0} --- clean_old'.format(fun.__name__)
                    _data_from_db = fun(self, *args, **kwargs)
                    _data_to_cache = {
                        'data': _data_from_db,
                        'last_query_time': str(time.time()),  # 刷新时间
                        'last_use_date': datetime.datetime.now().strftime('%Y-%m-%d'),  # 最近一次使用的时间
                        'life': life  # 数据寿命，从最近一次使用的时间开始算
                    }
                    rsdb.hset(key, _field, json_encode(_data_to_cache))

                _thread_pool.submit(_start)

            # 从缓存拿取数据
            data_from_cache = rsdb.hget(key, _field)
            # 缓存中有数据
            if data_from_cache:
                data_dict = json_decode(data_from_cache)
                # 立即刷新
                if immediately_refresh is True:
                    # 后台更新数据
                    cache_data_in_background_thread()
                    # 返回旧数据
                    data_to_return = data_dict['data']
                # 不立即刷新
                else:
                    # 不过期
                    if timeout == 0:
                        # 更新缓存中的时间
                        data_to_cache = {
                            'data': data_dict['data'],
                            'last_query_time': str(time.time()),
                            'last_use_date': datetime.datetime.now().strftime('%Y-%m-%d'),
                            'life': life
                        }
                        rsdb.hset(key, _field, json_encode(data_to_cache))
                        # 返回的数据
                        data_to_return = data_dict['data']
                    # 要过期
                    else:
                        last_query_time = float(data_dict['last_query_time'])
                        now_time = time.time()
                        # 过期
                        if now_time - last_query_time > timeout:
                            # 数据过期，返回旧数据，更新缓存中的时间，以防止多次启动线程；启动线程，更新缓存
                            data_to_cache = {
                                'data': data_dict['data'],
                                'last_query_time': str(time.time()),
                                'last_use_date': datetime.datetime.now().strftime('%Y-%m-%d'),
                                'life': life
                            }
                            rsdb.hset(key, _field, json_encode(data_to_cache))
                            # 启动更新线程
                            cache_data_in_background_thread()
                            # 返回旧数据
                            data_to_return = data_dict['data']
                        # 未过期
                        else:
                            # 更新使用时间
                            data_to_cache = {
                                'data': data_dict['data'],
                                'last_query_time': data_dict['last_query_time'],
                                'last_use_date': datetime.datetime.now().strftime('%Y-%m-%d'),
                                'life': life
                            }
                            rsdb.hset(key, _field, json_encode(data_to_cache))
                            # 返回的数据
                            data_to_return = data_dict['data']
            # 数据不存在，从数库拿取数据，并缓存
            else:
                app_log.debug('<---------> get data from db <---------> {0} <--------->'.format(fun.__name__))
                data_from_db = fun(self, *args, **kwargs)
                data_to_cache = {
                    'data': data_from_db,
                    'last_query_time': str(time.time()),
                    'last_use_date': datetime.datetime.now().strftime('%Y-%m-%d'),
                    'life': life
                }
                rsdb.hset(key, _field, json_encode(data_to_cache))
                data_to_return = data_from_db

            # 清除过期数据
            clean_old_cached_data(key=LCIC_MAIN_TEMP_FIXED_INFO_KEY)
            # 返回数据
            return data_to_return

        return decorators

    return cache_to_redis
