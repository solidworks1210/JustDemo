# coding=utf-8
# !/usr/bin/env python
#
# Copyright 2013 Stoneopus
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

"""
A lightweight wrapper around pymysql, 同步
1、该层直接操作数据库，所有调用该层的调用者只关心操作是否成功，不用关心异常
"""

from __future__ import absolute_import, division, with_statement

import itertools
import logging
import time
import traceback

try:
    # import mysql.connector as mysql_connector
    import pymysql as mysql_connector

except ImportError:
    raise


class Connection(object):

    def __init__(self, user, password, database, host='127.0.0.1', port=3306, max_idle_time=2 * 3600, **kwargs):
        """

        :param user: 数库用户
        :param password: 用户密码
        :param host: 主机
        :param port: 数据库监听的端口
        :param database: 要是用的数据库
        :param max_idle_time:
        :param kwargs: autocommit 自动提交
        """
        self.host = host
        self.database = database
        self.max_idle_time = float(max_idle_time)

        args = dict(
            host=host,
            port=int(port),
            user=user,
            password=password,
            database=database,
            use_unicode=True
        )

        self._db = None  # 保存的数据库连接对象
        self._db_args = args
        self._last_use_time = time.time()
        self._kwargs = kwargs
        try:
            self.reconnect()
        except:
            traceback.print_exc()
            logging.error("Cannot connect to MySQL on %s", self.host, exc_info=True)

    def __del__(self):
        self.close()

    def _ensure_connected(self):
        if self._db is None or (time.time() - self._last_use_time > self.max_idle_time):
            self.reconnect()
        self._last_use_time = time.time()

    def _cursor(self):
        """获取cursor对象，每执行一个数据库操作均须获取cursor，用完关闭"""
        self._ensure_connected()
        return self._db.cursor()

    def _cursor_close(self, cursor):
        """

        :param cursor: cursor 对象
        :return:
        """
        try:
            cursor.close()
        except:
            traceback.print_exc()
            logging.exception(traceback.format_exc())

    def _execute(self, cursor, query, args, kwargs):
        """
        select * from table where id=%s; -> args, list
        select * from table where id=%(xx)s; -> kwargs, dict
        :param cursor: cursor对象
        :param query: 执行的sql语句
        :param args:
        :param kwargs: 这两个参数不能同时使用
        :return:
        """
        try:
            return cursor.execute(query, kwargs or args)
        except:
            traceback.print_exc()
            logging.exception(traceback.format_exc())
            raise

    def close(self):
        """Closes this database connection."""
        if getattr(self, "_db", None) is not None:
            try:
                self._db.close()
            except:
                traceback.print_exc()
                logging.exception(traceback.format_exc())
        self._db = None

    def reconnect(self):
        """Closes the existing database connection and re-opens it."""
        self.close()
        self._db = mysql_connector.connect(**self._db_args)
        if self._kwargs.get('autocommit', False):
            # It's not a good idea to autocommit
            self._db.autocommit = True

    def commit(self):
        return self._db.commit()

    def rollback(self):
        return self._db.rollback()

    # -------------------------------------------------------------------------------------------

    def query(self, query, *args, **kwargs):
        """
        Returns a row list for the given query and parameters.(select result list(dict))
        :param query:
        :param args:
        :param kwargs:
        :return: [{}, {}, ...]
        """

        class Row(dict):
            """A dict that allows for object-like property access syntax."""

            def __getattr__(self, name):
                try:
                    return self[name]
                except KeyError:
                    raise AttributeError(name)

        # 获取courser
        cursor = self._cursor()
        # 数库操作
        try:
            self._execute(cursor, query, args, kwargs)
            column_names = [d[0] for d in cursor.description]
            return [Row(itertools.izip(column_names, row)) for row in cursor]
        except:
            traceback.print_exc()
            logging.exception(traceback.format_exc())
            return -1
        # 关闭courser
        finally:
            self._cursor_close(cursor)

    def insert_one(self, table, **kwargs):
        """
        插入一条到数据库
        :param table: 要保存的表
        :param kwargs:
        :return: False -1, True other
        """
        tag = False
        # 获取courser
        cursor = self._cursor()
        # 数库操作
        try:
            if len(kwargs) > 0:
                keys, parameters, params = '', '', []
                for key, value in kwargs.iteritems():
                    keys = keys + key + ', '
                    params.append(value)
                    parameters = parameters + '%s' + ', '
                keys = keys[:-2]  # 最后一个逗号不要
                parameters = parameters[:-2]
                sql = 'insert into ' + table + ' ( ' + keys + ' )' + ' values ' + '( ' + parameters + ' )'
                # 执行操作
                tag = True
                self._execute(cursor, sql, params, {})
                rowcount = cursor.rowcount
                self.commit()
                return rowcount
            else:
                raise AttributeError('insert_one, has no kwargs')
        except:
            if not tag:
                self.rollback()
            traceback.print_exc()
            logging.exception(traceback.format_exc())
            return -1
        # 关闭cursor
        finally:
            self._cursor_close(cursor)

    def insert_one_id(self, table, **kwargs):
        """
        插入一条记录，并返回自增id
        :param table:
        :param kwargs:
        :return:
        """
        result_insert = self.insert_one(table, **kwargs)
        if result_insert == -1:
            return -1

    def delete_one(self, table, **kwargs):
        """

        :param table:
        :param kwargs:
        :return:
        """
        tag = False
        # 获取courser
        cursor = self._cursor()
        # 数库操作
        try:
            if len(kwargs) > 0:
                keys, parameters, params = '', '', []
                for key, value in kwargs.iteritems():
                    params.append(value)
                    parameters = parameters + key + '=%s' + 'and '
                parameters = parameters[:-4]
                sql = 'delete from ' + table + ' where ' + parameters + ';'
                # 执行操作
                tag = True
                self._execute(cursor, sql, params, {})
                rowcount = cursor.rowcount
                self.commit()
                return rowcount
            else:
                raise AttributeError('delete_one, has no kwargs')
        except:
            if not tag:
                self.rollback()
            traceback.print_exc()
            logging.exception(traceback.format_exc())
            return -1
        # 关闭cursor
        finally:
            self._cursor_close(cursor)

    def update_one(self, table, id_item, **kwargs):
        """
        对execute_rowcount的一个封装
        :param table:
        :param id_item:
        :param kwargs:
        :return:
        """
        if len(kwargs) > 0:
            try:
                str_key = ''
                params = []
                for key, value in kwargs.iteritems():
                    str_key = str_key + key + '=%s, '
                    params.append(value)
                str_key = str_key[:-2]

                # 为了安全，如果id_item是字符串，去除 =
                if isinstance(id_item, type('')):
                    id_item = id_item.replace('=', '')
                elif isinstance(id_item, type(u'')):
                    id_item = id_item.replace(u'=', u'')
                sql = 'update ' + table + ' set ' + str_key + ' where id=' + id_item
                result = self.execute_rowcount(sql, *params)
                self.commit()
                return result
            except Exception as e:
                print __name__, '更新条目出错：', e
                self.rollback()
                return -1
        else:
            return -1

    # update = execute_rowcount
    # updatemany = executemany_rowcount
    #
    # insert = execute_rowcount
    # insertmany = executemany_lastrowid
