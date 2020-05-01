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


@app_views.route('/users',
                 methods=['GET'], strict_slashes=False)
def all_users():
    """ retrieves list of all users """
    users_all = storage.all('User')
    users_list = []
    for user in users_all.values():
        users_list.append(user.to_dict())
    return jsonify(users_list)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def one_user(user_id):
    """ retrieves one user """
    user_one = storage.get(User, user_id)
    if user_one is None:
        abort(404)
    return jsonify(user_one.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def del_user(user_id):
    """ deletes one user """
    user_del = storage.get(User, user_id)
    if user_del is None:
        abort(404)
    else:
        storage.delete(user_del)
        storage.save()
        answer = {}
        return jsonify(answer)


@app_views.route('/users', methods=['POST'],
                 strict_slashes=False)
def create_user():
    """ request to create a user """
    new_user = request.get_json(silent=True)
    if new_user is None:
        return "Not a JSON", 400
    if 'email' not in new_user:
        return ("Missing email", 400)
    if 'password' not in new_user:
        return ("Missing password", 400)
    user_created = User(**new_user)
    storage.new(user_created)
    storage.save()
    return jsonify(user_created.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'],
                 strict_slashes=False)
def update_user(user_id):
    """ updates the user object """
    upd_user = request.get_json(silent=True)
    if upd_user is None:
        return "Not a JSON", 400
    user_to_update = storage.get(User, user_id)
    if user_to_update is None:
        abort(404)
    list_ignore = ['id', 'updated_at', 'created_at', 'email']
    user_to_update.save()
    for key, value in upd_user.items():
        if key not in list_ignore:
            setattr(user_to_update, key, value)
    storage.save()
    return jsonify(user_to_update.to_dict())
