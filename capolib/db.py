# -*- coding: utf-8 -*-

"""
Persistence for Capo, including various conversion functions and model classes.
"""

from __future__ import absolute_import

from collections import namedtuple
from os.path import abspath, exists
import sqlite3

import capolib

# pylint: disable-msg=invalid-name
Runner = namedtuple("Runner", ['id', 'name'])
Race = namedtuple("Race", ['id', 'race_date', 'distance_km'])
Result = namedtuple("Result", ['race_id', 'race_date', 'runner_id',
                               'runner_name', 'race_duration_seconds'])


def format_time(secs):
    """
    Formats secs, a number as either 'm:ss' or 'h:mm:ss' if over
    one-hour's duration.
    """
    if secs < 3600:
        return '{m}:{s:02}'.format(m=secs//60, s=secs % 60)
    else:
        hours = secs // 3600
        mins = (secs - (hours * 3600)) // 60
        secs = (secs - (hours * 3600)) - (mins * 60)
        return '{h}:{m:02}:{s:02}'.format(h=hours, m=mins, s=secs)


def parse_time(t_str):
    """
    Parses a time string to an int containing the number of seconds. Supported
    input formats are 'h:mm:ss' and 'm:ss'.
    """
    parts = reversed(t_str.split(':'))
    return sum(int(part) * (60 ** index) for index, part in enumerate(parts))


class CapoDB(object):
    """
    Storage engine for Capo data.
    """
    def __init__(self, path='capo.sqlite'):
        """
        Connect to a Capo database, creating a new file if necessary.

        path defaults to 'capo.sqlite' in the current directory if not provided
        """
        if path != ':memory:':
            self._path = abspath(path)
            create_db = not exists(path)
        else:
            self._path = ':memory:'
            create_db = True

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
        return [Runner(*r) for r in runners]    # pylint: disable-msg=star-args

    def complete_runner(self, prefix):
        """
        Returns all runner names that begin with the supplied prefix.
        """
        runners = self._db.execute(
            "SELECT name FROM person WHERE name LIKE '{prefix}%'"
            .format(prefix=prefix))
        return [r[0] for r in runners]

    def races(self):
        """
        Return a sequence of Race objects for each stored race.
        """
        races = self._db.execute("SELECT race_id, race_date, distance_km "
                                 "FROM race ORDER BY race_date")
        return [Race(*r) for r in races]    # pylint: disable-msg=star-args

    def results(self, race_id):
        """
        Return a sequence of Result objects for a specified race.
        """
        results = self._db.execute("SELECT * FROM results WHERE race_id = ? "
                                   "ORDER BY race_date", (race_id,))
        return [Result(*r) for r in results]    # pylint: disable-msg=star-args

    def next_handicap(self, runner_id, for_race_date=None):
        """
        Calculate an estimated time for the next race (or the date provided as
        'for_race_date', if provided.

        for_race_date should be formatted as yyyy-mm-dd
        """
        if for_race_date is None:
            results = self._db.execute("SELECT race_duration_secs "
                                       "FROM results "
                                       "WHERE runner_id = ? "
                                       "ORDER BY race_date DESC LIMIT 3",
                                       (runner_id,))
        else:
            results = self._db.execute("SELECT race_duration_secs "
                                       "FROM results "
                                       "WHERE runner_id = ? "
                                       "AND race_date < ? "
                                       "ORDER BY race_date DESC LIMIT 3",
                                       (runner_id, for_race_date))
        durations = [r[0] for r in results]
        return sum(durations) / float(len(durations))

    def insert_test_data(self):
        """
        Load test data into the database
        """
        test_script = open(capolib.data_file('testdata.sql')).read()
        self._db.executescript(test_script)

    def add_person(self, name, time_estimate=None):
        cur = None
        try:
            cur = self._db.cursor()
            cur.execute('INSERT INTO person (name) VALUES (?)', (name,))
            person_id = cur.lastrowid
            if time_estimate is not None:
                cur.execute('INSERT INTO race_time '
                            '(race_id, person_id, race_duration_secs) '
                            'VALUES (?, ?, ?)', (0, person_id, time_estimate))
            self._db.commit()
            return person_id
        finally:
            if cur:
                cur.close()

    def add_race_time(self, race_id, person_id, time):
        cur = None
        try:
            cur = self._db.cursor()
            cur.execute('INSERT INTO race_time '
                        '(race_id, person_id, race_duration_secs) '
                        'VALUES (?, ?, ?)', (race_id, person_id, time))
            self._db.commit()
        finally:
            if cur:
                cur.close()