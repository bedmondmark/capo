# -*- coding: utf-8 -*-

from __future__ import absolute_import
from os.path import join as join_path
import unittest

class dbTestCase(unittest.TestCase):
    @property
    def _db(self):
        import capolib.db
        return capolib.db

    def test_format_time(self):
        format_time = self._db.format_time
        self.assertEqual(format_time(0), '0:00')
        self.assertEqual(format_time(1), '0:01')
        self.assertEqual(format_time(10), '0:10')
        self.assertEqual(format_time(59), '0:59')
        self.assertEqual(format_time(60), '1:00')
        self.assertEqual(format_time(61), '1:01')
        self.assertEqual(format_time(601), '10:01')
        self.assertEqual(format_time(3600), '1:00:00')
        self.assertEqual(format_time(3601), '1:00:01')
        self.assertEqual(format_time(3660), '1:01:00')
        self.assertEqual(format_time(3661), '1:01:01')

    def test_parse_time(self):
        parse_time = self._db.parse_time
        self.assertEqual(0, parse_time('0:00'))
        self.assertEqual(1, parse_time('0:01'))
        self.assertEqual(10, parse_time('0:10'))
        self.assertEqual(59, parse_time('0:59'))
        self.assertEqual(60, parse_time('1:00'))
        self.assertEqual(61, parse_time('1:01'))
        self.assertEqual(601, parse_time('10:01'))
        self.assertEqual(3600, parse_time('1:00:00'))
        self.assertEqual(3601, parse_time('1:00:01'))
        self.assertEqual(3660, parse_time('1:01:00'))
        self.assertEqual(3661, parse_time('1:01:01'))


class CapoDBTestCase(unittest.TestCase):
    @property
    def _db(self):
        import capolib.db
        return capolib.db

    def setUp(self):
        self.cdb = self._db.CapoDB(':memory:')
        self.cdb.insert_test_data()

    def test_runners(self):
        self.assertEqual(['Chris', 'James', 'Mark', 'Martin'],
                         list(r.name for r in self.cdb.runners()))

    def test_races(self):
        self.assertEqual(
            [self._db.Race(id=0, race_date=u'0000-00-00', distance_km=5),
             self._db.Race(id=1, race_date=u'2013-01-05', distance_km=5),
             self._db.Race(id=2, race_date=u'2013-02-06', distance_km=5)],
            list(self.cdb.races()))

    def test_results(self):
        self.assertEqual(2, len(self.cdb.results(1)))
        self.assertEqual(2, len(self.cdb.results(2)))

    def test_next_handicap(self):
        self.assertEqual(1307.5, self.cdb.next_handicap(1))
        self.assertEqual(1320.0, self.cdb.next_handicap(1, '2013-02-06'))

    def test_add_person(self):
        self.assertNotEqual(self.cdb.add_person('TestPerson'), None)


class CapoCmdTestCase(unittest.TestCase):
    @property
    def _console(self):
        import capolib.console
        return capolib.console

    def test_import(self):
        self._console


class InitTestCase(unittest.TestCase):
    @property
    def _capolib(self):
        import capolib
        return capolib

    def test_data_file(self):
        self.assertTrue(
            self._capolib.data_file('thing.sql')
            .endswith(join_path('capolib', 'data', 'thing.sql'))
        )

if __name__ == '__main__':
    unittest.main()