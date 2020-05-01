#!/usr/bin/python3
""" State objects that handles all default RestFul API actions
"""
from flask import Flask, jsonify, abort, request
from models import storage
from models.base_model import *
from models.state import State
from api.v1.views import app_views
from models.city import City
from models.amenity import Amenity


@app_views.route('/amenities',
                 methods=['GET'], strict_slashes=False)
def all_amenities():
    """ retrieves list of all amenities """
    amenities_all = storage.all('Amenity')
    amenity_list = []
    for amenity in amenities_all.values():
        amenity_list.append(amenity.to_dict())
    return jsonify(amenity_list)


@app_views.route('/amenities/<amenity_id>',
                 methods=['GET'], strict_slashes=False)
def one_amenity(amenity_id):
    """ retrieves one amenity """
    amenity_one = storage.get(Amenity, amenity_id)
    if amenity_one is None:
        abort(404)
    return jsonify(amenity_one.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def del_amenity(amenity_id):
    """ deletes one amenity """
    amenity_del = storage.get(Amenity, amenity_id)
    if amenity_del is None:
        abort(404)
    else:
        storage.delete(amenity_del)
        storage.save()
        answer = {}
        return jsonify(answer)


@app_views.route('/amenities', methods=['POST'],
                 strict_slashes=False)
def create_amenity():
    """ request to create a amenity """
    new_amenity = request.get_json(silent=True)
    if new_amenity is None:
        return "Not a JSON", 400
    if 'name' in new_amenity:
        amenity_created = Amenity(**new_amenity)
        storage.new(city_created)
        storage.save()
        return jsonify(amenity_created.to_dict()), 201
    else:
        return ("Missing name", 400)


@app_views.route('/cities/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def update_amenity(amenity_id):
    """ updates the amenity objects """
    upd_amenity = request.get_json(silent=True)
    if upd_amenity is None:
        return "Not a JSON", 400
    amenity_to_update = storage.get(Amenity, amenity_id)
    if amenity_to_update is None:
        abort(404)
    list_ignore = ['id', 'updated_at', 'created_at']
    amenity_to_update.save()
    for key, value in upd_amenity.items():
        if key not in list_ignore:
            setattr(amenity_to_update, key, value)
    storage.save()
    return jsonify(amenity_to_update.to_dict())
