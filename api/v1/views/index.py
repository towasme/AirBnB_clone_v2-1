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


@app_views.route('/stats')
def stats():
    """ retrieves number of objects by type """
    count_obj = {}
    plurals = {
        "Amenity": "amenities",
        "City": "cities",
        "Place": "places",
        "Review":  "reviews",
        "State": "states",
        "User": "users"
    }
    for key, value in plurals.items():
        count_obj[value] = storage.count(key)
    return jsonify(count_obj)
