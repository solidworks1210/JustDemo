# -*- coding:utf-8 -*-
# --------------------
# Author:		Ken
# Description:	数据库连接
# --------------------

import redis

import utils.tornpg
from conf.config import (POSTGRES_HOST, POSTGRES_PORT, POSTGRES_USER,
                         POSTGRES_DB, POSTGRES_PWD, REDIS_URL)

# Postgres connection user tornpg
psdb = utils.tornpg.Connection(
    host=POSTGRES_HOST,
    database=POSTGRES_DB,
    user=POSTGRES_USER,
    password=POSTGRES_PWD,
    port=POSTGRES_PORT)

# （用于缓存刷新）
psdb_for_update_cache = utils.tornpg.Connection(
    host=POSTGRES_HOST,
    database=POSTGRES_DB,
    user=POSTGRES_USER,
    password=POSTGRES_PWD,
    port=POSTGRES_PORT
)

# Redis connection
rsdb = redis.StrictRedis.from_url(REDIS_URL)
