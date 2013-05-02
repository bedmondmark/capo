#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Capo is your friendly handicap-race manager.
"""

from __future__ import absolute_import

import sys
import argparse
from capolib.console import CapoCmd


def main(argv=sys.argv[1:]):
    """
    Entry point for Capo.
    """
    arg_parser = argparse.ArgumentParser(description="Run Capo")
    arg_parser.add_argument('command', default='console', nargs='?', choices=['web', 'console'])
    args = arg_parser.parse_args(argv)

    if args.command == 'web':
        print >>sys.stderr, 'Web support not yet implemented.'
        return -1
    elif args.command == 'console':
        driver = CapoCmd('capo.sqlite')
        try:
            driver.cmdloop()
        except KeyboardInterrupt:
            print
        return 0


if __name__ == '__main__':
    sys.exit(main())
