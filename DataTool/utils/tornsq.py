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

"""A lightweight wrapper around sqlite3
"""

from __future__ import absolute_import, division, with_statement

import itertools
import time

try:
    import sqlite3 as db_connector
except ImportError:
    raise

version = "0.1"
version_info = (0, 1, 2, 0)


class Connection(object):
    """
    关闭自动提交
    """

    def __init__(self, db_path, timeout=5, max_idle_time=2 * 3600):
        """

        :param db_path: 数据库路径
        :param timeout: 连接等待锁定的持续时间，直到发生异常断开连接
        :param max_idle_time: timeout 参数默认是 5.0（5 秒）。
        """
        '''
        当一个数据库被多个连接访问，且其中一个修改了数据库，此时 SQLite 数据库被锁定，直到事务提交。
        timeout 参数表示连接等待锁定的持续时间，直到发生异常断开连接。timeout 参数默认是 5.0（5 秒）。
        '''
        self._db_path = db_path
        self.timeout = timeout
        self.max_idle_time = float(max_idle_time)
        self._last_use_time = time.time()

        # 保存数据库连接对象
        self._db = None

        # 建立数据库连接
        self.reconnect()

    def __del__(self):
        # 关闭数据库连接
        self.close()

    @staticmethod
    def _string_connect(*args):
        """
        拼接字符串：不同编码的可以比较，但不能直接拼接
        :return: 拼接好的字符串
        """
        result = ''
        for item in args:
            if isinstance(item, unicode):
                item = item.encode('utf-8')
            else:
                item = str(item)
            result += item
        return result

    def _ensure_connected(self):
        """
        长时间未操作，重连数据库
        :return:
        """
        time_idle = time.time() - self._last_use_time
        if self._db is None or time_idle > self.max_idle_time:
            self.reconnect()
        self._last_use_time = time.time()

    def _get_cursor(self):
        """
        获取数据库连接的cursor，以执行sql操作
        :return: cursor
        """
        # 确认连接
        self._ensure_connected()
        # 返回
        return self._db.cursor()

    @staticmethod
    def _close_cursor(cursor):
        """
        关闭数据库连接的cursor
        :param cursor:
        :return:
        """
        cursor.close()

    @staticmethod
    def _execute(cursor, sql, args, kwargs):
        """
        mysql、postgresql的占位符为%s，sqlite 为 ？，这个要注意
        :param cursor: 数据库cursor
        :param sql: 要执行的sql语句：
        :param args: type list, sql语句中占位符对应的值，与kwargs不能公用
        :param kwargs: type dict
        :return:
        """
        '''
        mysql、postgresql:
        select * from table where id=%s; list
        select * from table where id=%{name}s; dict
        sqlite:
        select * from table where id=?; list
        select * from table where id=:name; dict
        '''
        # 兼容mysql、posgresql
        execute_sql = sql.replace('%s', '?').replace('%{', ':').replace('}s', '')
        return cursor.execute(execute_sql, args or kwargs)

    def connect(self):
        """建立数据库连接"""
        return self.reconnect()

    def reconnect(self):
        """Closes the existing database connection and re-opens it."""
        # 关闭已有的连接
        self.close()
        # 建立新的连接
        self._db = db_connector.connect(self._db_path, timeout=self.timeout)
        # It's not a good idea to autocommit
        # self._db.autocommit = True

    def close(self):
        """Closes this database connection."""
        if getattr(self, "_db") is not None:
            self._db.close()
            self._db = None

    def commit(self):
        return self._db.commit()

    def rollback(self):
        return self._db.rollback()

    def query(self, sql, *args, **kwargs):
        """
        Returns a row list for the given query and parameters.(select result list(dict))
        :param sql:
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

        # 获取数据库连接的cursor
        cursor = self._get_cursor()
        # 执行sql操作，异常直接抛出
        try:
            self._execute(cursor, sql, args, kwargs)
            column_names = [d[0] for d in cursor.description]
            return [Row(itertools.izip(column_names, row)) for row in cursor]
        # 关闭数据库连接的cursor
        finally:
            self._close_cursor(cursor)

    def get(self, sql, *args, **kwargs):
        """

        :param sql:
        :param args:
        :param kwargs:
        :return: None 无结果，{} 一个值，raise 多个值
        """
        rows = self.query(sql, *args, **kwargs)
        if not rows:
            return None
        elif len(rows) > 1:
            raise Exception("Multiple rows returned for Database.get() query")
        else:
            return rows[0]

    def insert(self, table, auto_commit=True, **kwargs):
        """
        插入一条到数据库
        :param table: 要保存的表
        :param auto_commit: True 自动提交，False 手动提交
        :param kwargs: 键值对，键要与数据库对应
        :return: 返回受影响的行数 or 抛出异常
        """
        # 组装参数
        keys = ''
        placeholders = ''
        values = []
        for key, value in kwargs.iteritems():
            keys = keys + key + ', '
            values.append(value)
            placeholders = placeholders + '%s' + ', '
        keys = keys[:-2]  # 最后一个逗号不要
        placeholders = placeholders[:-2]
        # sql语句
        sql_insert = 'insert into {table} ({keys}) values ({placeholders})' \
            .format(**{'table': table, 'keys': keys, 'placeholders': placeholders})
        # 操作数据库
        cursor = self._get_cursor()
        try:
            # 执行sql
            self._execute(cursor, sql_insert, values, {})
            # 是否自动提交
            if auto_commit is True:
                self.commit()
            return cursor.rowcount
        except:
            # 异常时回滚
            if auto_commit is True:
                self.rollback()
            # 抛出异常，由调用者处理
            raise
        finally:
            # 关闭cursor
            self._close_cursor(cursor)

    def update(self, table, id_item, auto_commit=True, **kwargs):
        """
        通过唯一标识id更新记录
        :param table:
        :param id_item: 唯一标志
        :param auto_commit: True 自动提交，False 手动提交
        :param kwargs:
        :return:
        """
        str_key = ''
        values = []
        for key, value in kwargs.iteritems():
            str_key = str_key + key + '=%s, '
            values.append(value)
        str_key = str_key[:-2]
        # sql = 'update ' + table + ' set ' + str_key + ' where id=' + id_item
        # 为了安全，如果id_item是字符串，去除 =
        if isinstance(id_item, type('')):
            id_item = id_item.replace('=', '')
        elif isinstance(id_item, type(u'')):
            id_item = id_item.replace(u'=', u'')
        sql_update = self._string_connect('update ', table, ' set ', str_key, ' where id=', id_item)
        cursor = self._get_cursor()
        try:
            # 执行sql
            self._execute(cursor, sql_update, values, {})
            # 是否自动提交
            if auto_commit is True:
                self.commit()
            # 返回受影响的行数
            return cursor.rowcount
        except:
            # 异常时回滚
            if auto_commit is True:
                self.rollback()
            # 抛出异常，由调用者处理
            raise
        finally:
            # 关闭cursor
            self._close_cursor(cursor)

    def delete(self, table, id_item, auto_commit=True):
        """
        通过id删除记录
        :param table:
        :param id_item:
        :param auto_commit:
        :return:
        """
        sql_delete = "delete from {table} where id=%s;".format(**{'table': table})
        cursor = self._get_cursor()
        try:
            # 执行sql
            self._execute(cursor, sql_delete, id_item, {})
            # 是否自动提交
            if auto_commit is True:
                self.commit()
            # 返回受影响的行数
            return cursor.rowcount
        except:
            # 异常时回滚
            if auto_commit is True:
                self.rollback()
            # 抛出异常，由调用者处理
            raise
        finally:
            # 关闭cursor
            self._close_cursor(cursor)

    def execute(self, sql, *args, **kwargs):
        """
        执行sql, select直接调用query， （insert、update、delete）需手动提交
        :param sql:
        :param args:
        :param kwargs:
        :return: select返回查询结果；（insert、update、delete）返回受影响的行数
        """
        if 'select' in sql.lower():
            return self.query(sql, *args, **kwargs)
        else:
            cursor = self._get_cursor()
            try:
                # 执行sql
                self._execute(cursor, sql, args, kwargs)
                # 返回受影响的行数
                return cursor.rowcount
            finally:
                # 关闭cursor
                self._close_cursor(cursor)

    def original_query(self, sql, *args, **kwargs):
        """
        最原始的查询结果
        :param sql:
        :param args:
        :param kwargs:
        :return: [(), (), ()]
        """
        cursor = self._get_cursor()
        try:
            self._execute(cursor, sql, args, kwargs)
            return cursor.fetchall()
        finally:
            self._close_cursor(cursor)

    def count(self, sql, *args, **kwargs):
        """
        select count(*) from table where ....
        :param sql:
        :param args:
        :return: count 的值
        """
        cursor = self._get_cursor()
        try:
            self._execute(cursor, sql, args, kwargs)
            return cursor.fetchall()[0][0]
        finally:
            self._close_cursor(cursor)


if __name__ == '__main__':
    db = Connection('hello.sqlite')
    db.execute('DROP TABLE IF EXISTS `test`;')
    create_talbe_sql = '''create table `test`(
    id integer,
    name varchar(15) default 'h'
    )'''
    db.execute(create_talbe_sql)
