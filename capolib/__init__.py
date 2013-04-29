# -*- coding: utf-8 -*-

"""
capolib - logic and persistence engine for Capo.
"""

from os.path import join as join_path, dirname

def data_file(filename):
    '''
    Construct a path to a file in the 'data' directory contained within capolib.
    '''
    return join_path(dirname(__file__), 'data', filename)