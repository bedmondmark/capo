# -*- coding: utf-8 -*-

"""
capolib.web - Capo's web interface
"""

from __future__ import absolute_import

from flask import Flask

from . import views


def start():
    """
    Start the Capo web server.
    """
    app = Flask('capolib.web')
    views.init_views(app)
    app.run()
