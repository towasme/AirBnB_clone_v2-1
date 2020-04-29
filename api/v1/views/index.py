#!/usr/bin/python3
""" routes file to work with flask """

from api.v1.views import app_views


@app_views.route('/status')
def json_return:
    """ return a json status OK """
    status = {  "status": "OK"}
    return status
