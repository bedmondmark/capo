# -*- coding: utf-8 -*-

from __future__ import absolute_import

from collections import namedtuple
from os.path import abspath, exists
import sqlite3

import capolib


Runner = namedtuple("Runner", ['id', 'name'])
Race = namedtuple("Race", ['id', 'race_date', 'distance_km'])


class CapoDB(object):
    def __init__(self, path='capo.sqlite'):
        self._path = abspath(path)

        create_db = not exists(path)
        self._db = sqlite3.connect(path)
        if create_db:
            self._create()

    def _create(self):
            db_script = open(capolib.data_file('capo_ddl.sql')).read()
            self._db.executescript(db_script)

    def runners(self):
        runners = self._db.execute("SELECT "
                                   "person.person_id, person.name AS name "
                                   "FROM person ORDER BY person.name")
        return [Runner(*r) for r in runners]

    def races(self):
        races = self._db.execute("SELECT race_id, race_date, distance_km "
                                 "FROM race ORDER BY race_date")
        return [Race(*r) for r in races]

    def _insert_test_data(self):
        """
        Load test data into the database
        """
        test_script = open(capolib.data_file('testdata.sql')).read()
        self._db.executescript(test_script)