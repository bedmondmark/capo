#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Capo is your friendly handicap-race manager.
"""

from __future__ import absolute_import

import cmd
from textwrap import dedent

import capolib
import capolib.db


def command(func):
    """
    A decorator that reformats the wrapped function's docstring.
    """
    if func.__doc__:
        func.__doc__ = dedent(func.__doc__)
    return func


class CapoCmd(object, cmd.Cmd):
    """
    Logic engine for Capo's command-line input loop.
    """

    prompt = "capo> "
    intro = r"""
         _\|/_
         (o o)
 +----oOO-{_}-OOo------------------------------------------+
 |                     Welcome to Capo                     |
 |                     Oo-----------oO                     |
 |            Let me manage your handicap race.            |
 +---------------------------------------------------------+

 type 'help' for more instructions
 """

    def __init__(self, db_path):
        cmd.Cmd.__init__(self)
        self._db = capolib.db.CapoDB(db_path)

    @command
    @staticmethod
    def do_quit(line):
        """Quit capo."""
        print line
        return True

    do_exit = do_quit

    @command
    def do_runners(self, _):
        """
        List all known runners
        """
        for runner in self._db.runners():
            print runner.name

    @command
    def do_races(self, _):
        """
        List all the known races.

        This will show you the id, race date and distance for each race.
        """
        for race in self._db.races():
            print "{id:02d} {date} {distance}km".format(
                id=race.id,
                date=race.race_date,
                distance=race.distance_km)

    @command
    def do_testdata(self, _):
        """
        Load test data into the database
        """
        self._db.insert_test_data()


def main():
    """
    Entry point for Capo.
    """
    driver = CapoCmd('capo.sqlite')
    try:
        driver.cmdloop()
    except KeyboardInterrupt:
        print


if __name__ == '__main__':
    main()
