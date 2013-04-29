# -*- coding: utf-8 -*-

"""
Persistence for Capo, including various conversion functions and model classes.
"""

from __future__ import absolute_import

from collections import namedtuple
from os.path import abspath, exists
import sqlite3

import capolib

# pylint: disable-msg=C0103
Runner = namedtuple("Runner", ['id', 'name'])
Race = namedtuple("Race", ['id', 'race_date', 'distance_km'])


def format_time(secs):
    """
    Formats secs, a number as either 'm:ss' or 'h:mm:ss' if over
    one-hour's duration.
    """
    if secs < 3600:
        return '{m}:{s:02}'.format(m=secs//60, s=secs % 60)
    else:
        h = secs // 3600
        m = (secs - (h * 3600)) // 60
        s = (secs - (h * 3600)) - (m * 60)
        return '{h}:{m:02}:{s:02}'.format(h=h, m=m, s=s)


class CapoDB(object):
    """
    Storage engine for Capo data.
    """
    def __init__(self, path='capo.sqlite'):
        """
        Connect to a Capo database, creating a new file if necessary.

        path defaults to 'capo.sqlite' in the current directory if not provided
        """
        self._path = abspath(path)

        create_db = not exists(path)
        self._db = sqlite3.connect(path)
        if create_db:
            self._create()

    def _create(self):
        """
        Create a new database, for when one doesn't exist already.
        """
        db_script = open(capolib.data_file('capo_ddl.sql')).read()
        self._db.executescript(db_script)

    def runners(self):
        """
        Return a sequence of Runner objects for each stored person.
        """
        runners = self._db.execute("SELECT "
                                   "person.person_id, person.name AS name "
                                   "FROM person ORDER BY person.name")
        return [Runner(*r) for r in runners]

    def races(self):
        """
        Return a sequence of Race objects for each stored race.
        """
        races = self._db.execute("SELECT race_id, race_date, distance_km "
                                 "FROM race ORDER BY race_date")
        return [Race(*r) for r in races]

    def insert_test_data(self):
        """
        Load test data into the database
        """
        test_script = open(capolib.data_file('testdata.sql')).read()
        self._db.executescript(test_script)
