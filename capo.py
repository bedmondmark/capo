#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Capo is your friendly handicap-race manager.
"""

from __future__ import absolute_import

from capolib.console import CapoCmd


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
