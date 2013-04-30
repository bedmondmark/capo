# -*- coding: utf-8 -*-

"""
capolib.console - Console interface for Capo.
"""

import cmd
from textwrap import dedent
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

    def __init__(self, db_path, *args, **kwargs):
        cmd.Cmd.__init__(self, *args, **kwargs)
        self._db = capolib.db.CapoDB(db_path)

    @staticmethod
    @command
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

    def do_test(self, line):
        print line

    def complete_test(self, text, _line, _start, _end):
        return self._db.complete_runner(text)

    @command
    def do_testdata(self, _):
        """
        Load test data into the database
        """
        self._db.insert_test_data()
