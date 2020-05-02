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
from models.user import User
from models.place import Place


@app_views.route('/cities/<city_id>/places',
                 methods=['GET'], strict_slashes=False)
def all_places_in_city(city_id):
    """ retrieves list of all places in a city """
    city_exist = storage.get(City, city_id)
    if city_exist is None:
        abort(404)
    places_all = storage.all('Place')
    places_list = []
    for place in places_all.values():
        places_list.append(place.to_dict())
    return jsonify(places_list)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def one_place(place_id):
    """ retrieves one place """
    place_one = storage.get(Place, place_id)
    if place_one is None:
        abort(404)
    return jsonify(place_one.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def del_place(place_id):
    """ deletes one place """
    place_del = storage.get(Place, place_id)
    if place_del is None:
        abort(404)
    else:
        storage.delete(place_del)
        storage.save()
        answer = {}
        return jsonify(answer), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """ request to create a place """
    city_exist = storage.get(City, city_id)
    if city_exist is None:
        abort(404)
    new_place = request.get_json(silent=True)
    if new_place is None:
        return "Not a JSON", 400
    if 'user_id' not in new_place:
        return ("Missing user_id", 400)
    if 'name' not in new_place:
        return ("Missing name", 400)
    user_id = new_place['user_id']
    user_exist = storage.get(User, user_id)
    if user_exist is None:
        abort(404)
    new_place["city_id"] = city_id
    place_created = Place(**new_place)
    storage.new(place_created)
    storage.save()
    return jsonify(place_created.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'],
                 strict_slashes=False)
def update_place(place_id):
    """ updates the place object """
    upd_place = request.get_json(silent=True)
    if upd_place is None:
        return "Not a JSON", 400
    place_to_update = storage.get(Place, place_id)
    if place_to_update is None:
        abort(404)
    list_ignore = ['id', 'updated_at', 'created_at', 'user_id', 'city_id']
    place_to_update.save()
    for key, value in upd_place.items():
        if key not in list_ignore:
            setattr(place_to_update, key, value)
    storage.save()
    return jsonify(place_to_update.to_dict())
