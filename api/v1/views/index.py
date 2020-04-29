#!/usr/bin/python3
""" routes file to work with flask """

from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status')
def status():
    """ return a json status OK """
    answer = {"status": "OK"}
    return jsonify(answer)

