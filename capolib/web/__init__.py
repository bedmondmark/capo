# -*- coding: utf-8 -*-

from __future__ import absolute_import

from flask import Flask

from . import views

def start():
    app = Flask('capolib.web')
    views.init_views(app)
    app.run()