# -*- coding: utf-8 -*-

from __future__ import absolute_import
from os.path import join as join_path
import unittest

class DBTestCase(unittest.TestCase):
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