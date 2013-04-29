#!/usr/bin/env python
# -*- coding: utf-8 -*-

import capolib
import cmd
import os
from os.path import join as join_path, dirname
import sqlite3


DB_SCRIPT = open(capolib.data_file('capo.ddl')).read()


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

    def __init__(self, dbconn):
        cmd.Cmd.__init__(self)
        self._db = dbconn

    def do_quit(self, line):
        """ Stop Capo."""
        print line
        return True

    do_exit = do_quit

    def do_runners(self, line):
        """
        List all known runners
        """
        runners = self._db.execute("""SELECT person.name AS name FROM person""")
        for runner in runners:
            print runner[0]

    def do_races(self, line):
        """
        List all the known races
        """
        races = self._db.execute("""SELECT race_date, race_start_time""")

    def do_testdata(self, line):
        """
        Load test data into the database
        """
        test_script = open(capolib.data_file('testdata.sql')).read()
        self._db.executescript(test_script)


def main():
    new_db = not os.path.exists('capo.sqlite')

    dbconn = sqlite3.connect('capo.sqlite')
    if new_db:
        dbconn.executescript(DB_SCRIPT)

    driver = CapoCmd(dbconn)
    try:
        driver.cmdloop()
    except KeyboardInterrupt:
        print


if __name__ == '__main__':
    main()