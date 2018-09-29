#!/usr/bin/env python
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

"""A lightweight wrapper around mysql-connector-python.
"""

from __future__ import absolute_import, division, with_statement

import itertools
import logging
import time

try:
    import mysql.connector
    from mysql.connector import OperationalError
except ImportError:
    raise

version = "0.1"
version_info = (0, 1, 2, 0)


class Connection(object):
    """A lightweight wrapper around psycopg2 DB-API connections.

    The main value we provide is wrapping rows in a dict/object so that
    columns can be accessed by name. Typical usage::

        db = database.Connection("127.0.0.1", "mydb")
        for fish in db.query("SELECT * FROM fishes"):
            print fish.name

    Cursors are hidden by the implementation, but other than that, the methods
    are very similar to the DB-API.

    --We explicitly set the timezone to UTC and the character encoding to
    --UTF-8 on all connections to avoid time zone and encoding errors.
    """

    def __init__(self, host, database, port=None, user=None, password=None,
                 max_idle_time=2 * 3600):
        self.host = host
        self.database = database
        self.max_idle_time = float(max_idle_time)

        args = dict(use_unicode=True, database=database)
        if user is not None:
            args['user'] = user
        if password is not None:
            args['password'] = password

        # We accept a path to a host(:port) string
        pair = host.split(":")
        if len(pair) == 2:
            args['host'] = pair[0]
            args['port'] = port or int(pair[1])
        else:
            args['host'] = host
            args['port'] = port or 5432

        self._db = None
        self._db_args = args
        self._last_use_time = time.time()
        try:
            self.reconnect()
        except Exception:
            logging.error("Cannot connect to MySQL on %s", self.host,
                          exc_info=True)

    def __del__(self):
        self.close()

    def close(self):
        """Closes this database connection."""
        if getattr(self, "_db", None) is not None:
            self._db.close()
            self._db = None

    def reconnect(self):
        """Closes the existing database connection and re-opens it."""
        self.close()
        self._db = mysql.connector.connect(**self._db_args)
        # It's not a good idea to autocommit
        # self._db.autocommit = True

    def commit(self):
        """Commit any pending transaction to the database.
        By default, Psycopg opens a transaction before executing the first
        command: if commit() is not called, the effect of any data
        manipulation will be lost.

        The connection can be also set in "autocommit" mode: no transaction
        is automatically open, commands have immediate effect.
        """
        return self._db.commit()

    def rollback(self):
        """Roll back to the start of any pending transaction. Closing a
        connection without committing the changes first will cause an implicit
        rollback to be performed.
        Changed in psycopg2 version 2.5: if the connection is used in a with
        statement, the method is automatically called if an exception is raised
        in the with block.
        """
        return self._db.rollback()

    def query(self, query, *parameters, **kwparameters):
        """Returns a row list for the given query and parameters.(select result list(dict))"""
        cursor = self._cursor()
        try:
            self._execute(cursor, query, parameters, kwparameters)
            column_names = [d[0] for d in cursor.description]
            return [Row(itertools.izip(column_names, row)) for row in cursor]
        finally:
            cursor.close()

    def get(self, query, *parameters, **kwparameters):
        """Returns the (singular) row returned by the given query.

        If the query has no results, returns None. If it has
        more than one result, raises an exception.
        """
        rows = self.query(query, *parameters, **kwparameters)
        if not rows:
            return None
        elif len(rows) > 1:
            raise Exception("Multiple rows returned for Database.get() query")
        else:
            return rows[0]

    # rowcount is a more reasonable default return value than lastrowid,
    # but for historical compatibility execute() must return lastrowid.
    def execute(self, query, *parameters, **kwparameters):
        """Executes the given query, returning the lastrowid from the query."""
        return self.execute_lastrowid(query, *parameters, **kwparameters)

    def execute_lastrowid(self, query, *parameters, **kwparameters):
        """Executes the given query, returning the lastrowid from the query."""
        cursor = self._cursor()
        try:
            self._execute(cursor, query, parameters, kwparameters)
            return cursor.fetchone()
            # return cursor.lastrowid
        finally:
            cursor.close()

    def execute_rowcount(self, query, *parameters, **kwparameters):
        """Executes the given query, returning the rowcount from the query (insert, update,delete)"""
        cursor = self._cursor()
        try:
            self._execute(cursor, query, parameters, kwparameters)
            return cursor.rowcount
        finally:
            cursor.close()

    def executemany(self, query, parameters):
        """Executes the given query against all the given param sequences.

        We return the lastrowid from the query.
        """
        return self.executemany_lastrowid(query, parameters)

    def executemany_lastrowid(self, query, parameters):
        """Executes the given query against all the given param sequences.

        We return the lastrowid from the query.
        """
        cursor = self._cursor()
        try:
            cursor.executemany(query, parameters)
            return cursor.fetchone()
            # return cursor.lastrowid
        finally:
            cursor.close()

    def executemany_rowcount(self, query, parameters):
        """Executes the given query against all the given param sequences.

        We return the rowcount from the query.
        """
        cursor = self._cursor()
        try:
            cursor.executemany(query, parameters)
            return cursor.rowcount
        finally:
            cursor.close()

    update = execute_rowcount
    updatemany = executemany_rowcount

    insert = execute_rowcount
    insertmany = executemany_lastrowid

    def _ensure_connected(self):
        # Postgresql by default closes client connections that are idle for
        # 2 hours on linux, but the client library does not report this fact
        # until you try to perform a query and it fails.  Protect against
        # this case by preemptively closing and reopening the connection
        # if it has been idle for too long (7 hours by default).
        if (self._db is None or
                (time.time() - self._last_use_time > self.max_idle_time)):
            self.reconnect()
        self._last_use_time = time.time()

    def _cursor(self):
        self._ensure_connected()
        return self._db.cursor()

    def _execute(self, cursor, query, parameters, kwparameters):
        try:
            return cursor.execute(query, kwparameters or parameters)
        except OperationalError:
            logging.error("Error connecting to Postgresql on %s", self.host)
            self.close()
            raise

    def original_execute(self, query, *args, **kwargs):
        cursor = self._cursor()
        try:
            self._execute(cursor, query, args, kwargs)
            return cursor.fetchall()
        finally:
            cursor.close()

    def count(self, query, *args, **kwargs):
        """
        count(*)
        :param query:
        :param args:
        :return:
        """
        cursor = self._cursor()
        try:
            self._execute(cursor, query, args, kwargs)
            return cursor.fetchall()[0][0]
        finally:
            cursor.close()

class Row(dict):
    """A dict that allows for object-like property access syntax."""

    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError(name)
