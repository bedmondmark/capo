# -*- coding: utf-8 -*-

"""
capolib.web.views - Provides all of Capo's Flask views.
"""

from flask import render_template


def init_views(app):
    """
    Create all the required views on the supplied Flask app.
    """
    # pylint: disable-msg=unused-variable

    @app.route('/')
    def index():
        """
        The initial view for the application.
        """
        return render_template('index.html')
