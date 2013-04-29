# -*- coding: utf-8 -*-

from __future__ import absolute_import
import unittest


class format_time_TestCase(unittest.TestCase):
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

if __name__ == '__main__':
    unittest.main()