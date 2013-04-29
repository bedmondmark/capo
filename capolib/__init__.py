# -*- coding: utf-8 -*-

from os.path import join as join_path, dirname

def data_file(fn):
    return join_path(dirname(__file__), 'data', fn)