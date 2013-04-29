#!/usr/bin/env python
# -*- coding: utf-8 -*-

import capolib
import capolib.db
import cmd
from textwrap import dedent


def command(f):
    """
    A decorator that reformats the wrapped function's docstring.
    """
    if f.__doc__:
        f.__doc__ = dedent(f.__doc__)
    return f


class CapoCmd(object, cmd.Cmd):
    prompt = "capo> "
    intro = """
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
    def do_quit(self, line):
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
        self._db._insert_test_data()


def main():
    driver = CapoCmd('capo.sqlite')
    try:
        driver.cmdloop()
    except KeyboardInterrupt:
        print


if __name__ == '__main__':
    main()