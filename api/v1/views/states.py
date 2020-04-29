#!/usr/bin/python3
""" State objects that handles all default RestFul API actions
"""
from flask import Flask, jsonify, abort
from models import storage
from models.base_model import *
from models.state import State


@app.route('/states', methods=['GET'], strict_slashes=False)
def all_state():
    """ retrieves list of all states """
    all_states = storage.all(State)
    states_list = []
    for state in all_states.values():
        states_list.append = state.to_dict()
    return jsonify(states_list)


@app.route('/api/v1/states/<state_id>', methods=['GET'], strict_slashes=False)
def one_state(state_id):
    """ retrieves one state """
    state_one = storage.get(State, state_id)
    if state_one is None:
        abort(404)
    return jsonify(state_one.to_dict())
