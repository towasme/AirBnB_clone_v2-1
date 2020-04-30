#!/usr/bin/python3
""" State objects that handles all default RestFul API actions
"""
from flask import Flask, jsonify, abort, request
from models import storage
from models.base_model import *
from models.state import State
from api.v1.views import app_views
from models.city import City


@app_views.route('/states/<state_id>/cities',
                 methods=['GET'], strict_slashes=False)
def all_cities_from_state(state_id):
    """ retrieves list of all states """
    state_exist = storage.get(State, state_id)
    if state_exist is None:
        abort(404)
    all_cities = storage.all('City')
    cities_list = []
    for city in all_cities.values():
        if city.state_id == state_id:
            cities_list.append(city.to_dict())
    return jsonify(cities_list)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def one_city(city_id):
    """ retrieves one city """
    city_one = storage.get(City, city_id)
    if city_one is None:
        abort(404)
    return jsonify(city_one.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def del_city(city_id):
    """ deletes one city """
    city_del = storage.get(City, city_id)
    if city_del is None:
        abort(404)
    else:
        storage.delete(city_del)
        storage.save()
        answer = {}
        return jsonify(answer)


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def create_city(state_id):
    """ request to create a city """
    state_name_exist = storage.get(State, state_id)
    if state_name_exist is None:
        abort(404)
    new_city = request.get_json(silent=True)
    if new_city is None:
        return "Not a JSON", 400
    if 'name' in new_city:
        new_city['state_id'] = state_id
        city_created = City(**new_city)
        storage.new(city_created)
        storage.save()
        return jsonify(city_created.to_dict()), 201
    else:
        return ("Missing name", 400)


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """ updates the city objects """
    upd_city = request.get_json(silent=True)
    if upd_city is None:
        return "Not a JSON", 400
    city_to_update = storage.get(City, city_id)
    if city_to_update is None:
        abort(404)
    list_ignore = ['id', 'state_id', 'updated_at', 'created_at']
    city_to_update.save()
    for key, value in upd_city.items():
        if key not in list_ignore:
            setattr(city_to_update, key, value)
    storage.save()
    return jsonify(city_to_update.to_dict())
