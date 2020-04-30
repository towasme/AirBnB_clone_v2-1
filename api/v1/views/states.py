#!/usr/bin/python3
""" State objects that handles all default RestFul API actions
"""
from flask import Flask, jsonify, abort, request
from models import storage
from models.base_model import *
from models.state import State
from api.v1.views import app_views


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def all_state():
    """ retrieves list of all states """
    all_states = storage.all(State)
    states_list = []
    for state in all_states.values():
        states_list.append(state.to_dict())
    return jsonify(states_list)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def one_state(state_id):
    """ retrieves one state """
    state_one = storage.get(State, state_id)
    if state_one is None:
        abort(404)
    return jsonify(state_one.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def del_state(state_id):
    """ deletes one state """
    state_del = storage.get(State, state_id)
    if state_del is None:
        abort(404)
    else:
        storage.delete(state_id)
        storage.save()
        answer = {}
        return jsonify(answer)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """ request to create a state """
    new_state = request.get_json(silent=True)
    if new_state is None:
        return "Not a JSON", 400
    if 'name' in new_state:
        state_created = State(**new_state)
        storage.new(state_created)
        storage.save()
        return jsonify(state_created.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """ updates the state objects """
    upd_state = request.get_json(silent=True)
    if upd_state is None:
        return "Not a JSON", 400
    state_to_update = storage.get(State, state_id)
    if state_to_update is None:
        abort(404)
    list_ignore = ['created_at', 'id', 'updated_at']
    for key, value in upd_state.items():
        if key not in list_ignore:
            setattr(state_to_update, key, value)
    storage.save()
    return jsonify(state_to_update.to_dict())
