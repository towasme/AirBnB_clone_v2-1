#!/usr/bin/python3
""" routes file to work with flask """

from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status')
def status():
    """ return a json status OK """
    answer = {"status": "OK"}
    return jsonify(answer)


@app_views.route('/api/v1/stats')
def stats():
    """ retrieves number of objects by type """
    return storage.count()
