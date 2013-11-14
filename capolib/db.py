# -*- coding: utf-8 -*-

"""
Persistence for Capo, including various conversion functions and model classes.
"""

from __future__ import absolute_import

from os.path import abspath, exists

import peewee


db = peewee.SqliteDatabase(None)


class Model(peewee.Model):
    class Meta:
        database = db


class Person(Model):
    id = peewee.PrimaryKeyField()
    name = peewee.CharField()

    def next_handicap(self, for_race_date=None):
        """
        Calculate an estimated time for the next race (or the date provided as
        'for_race_date', if provided.

        for_race_date should be formatted as yyyy-mm-dd
        """
        query = (RaceEntry.select().join(Race).where(RaceEntry.runner == self))
        if for_race_date is not None:
            query = query.where(Race.race_date < for_race_date)

        query = (query.order_by(Race.race_date.desc()).limit(3))
        durations = [r.actual_time for r in query]
        if durations:
            return sum(durations) / float(len(durations))
        return None

    class Meta:
        order_by = ('name', )


class Race(Model):
    id = peewee.PrimaryKeyField()
    race_date = peewee.DateField()
    distance_km = peewee.FloatField()

    def __repr__(self):
        return "Race(id={}, distance_km={}, race_date={})".format(
            self.id, self.distance_km, self.race_date
        )


class RaceEntry(Model):
    id = peewee.PrimaryKeyField()
    race = peewee.ForeignKeyField(Race, related_name='entries')
    runner = peewee.ForeignKeyField(Person, related_name='entries')
    estimated_time = peewee.IntegerField()
    actual_time = peewee.IntegerField(null=True)


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
            self._path = path
            create_db = True

        db.init(self._path)
        db.connect()

        if create_db:
            self._create()

    def _create(self):
        """
        Create a new database, for when one doesn't exist already.
        """
        #db_script = open(capolib.data_file('capo_ddl.sql')).read()
        #self._db.executescript(db_script)
        Person.create_table(True)
        Race.create_table(True)
        RaceEntry.create_table(True)

        Race.create(id=0, race_date=u'0000-00-00', distance_km=5)

    def runners(self):
        """
        Return a sequence of Runner objects for each stored person.
        """
        return Person.select().order_by(Person.name)

    def complete_runner(self, prefix):
        """
        Returns all runner names that begin with the supplied prefix.
        """
        runners = Person.select(Person.name).where(
            peewee.fn.Substr(Person.name, 1, len(prefix)) == prefix)
        return [r.name for r in runners]

    def races(self):
        """
        Return a sequence of Race objects for each stored race.
        """
        return Race.select()

    def results(self, race_id):
        """
        Return a sequence of Result objects for a specified race.
        """
        return list(Race.get(Race.id == race_id).entries)

    def next_handicap(self, runner_id, for_race_date=None):
        """
        Calculate an estimated time for the next race (or the date provided as
        'for_race_date', if provided.

        for_race_date should be formatted as yyyy-mm-dd
        """
        return (Person.get(Person.id == runner_id)
                .next_handicap(for_race_date))

    def insert_test_data(self):
        """
        Load test data into the database
        """
        pass

    def add_person(self, name, time_estimate=None):
        """
        Add a new person to the datastore. The returned value is the id
        for the new person record.
        """
        with db.transaction():
            person = Person(name=name)
            # TODO: The following:
            # if time_estimate is not None:
            #     pass
            person.save()
        return person

    def add_race_time(self, race_id, person_id, time):
        """
        Store a race time for the person and race specified.
        """
        self._db.execute('INSERT INTO race_time '
                    '(race_id, person_id, race_duration_secs) '
                    'VALUES (?, ?, ?)', (race_id, person_id, time))
        self._db.commit()