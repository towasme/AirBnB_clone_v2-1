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
from models.review import Review


@app_views.route('/places/<place_id>/reviews',
                 methods=['GET'], strict_slashes=False)
def all_reviews(place_id):
    """ retrieves list of all reviews from a place """
    place_exist = storage.get(Place, place_id)
    if place_exist is None:
        abort(404)
    reviews_all = storage.all('Review')
    review_list = []
    for review in reviews_all.values():
        if review.place_id == place_id:
            review_list.append(review.to_dict())
    return jsonify(review_list)


@app_views.route('/reviews/<review_id>',
                 methods=['GET'], strict_slashes=False)
def one_review(review_id):
    """ retrieves one review """
    review_one = storage.get(Review, review_id)
    if review_one is None:
        abort(404)
    return jsonify(review_one.to_dict())


@app_views.route('/reviews/<review_id>',
                 methods=['DELETE'],
                 strict_slashes=False)
def del_review(review_id):
    """ deletes one review """
    review_del = storage.get(Review, review_id)
    if review_del is None:
        abort(404)
    else:
        storage.delete(review_del)
        storage.save()
        answer = {}
        return jsonify(answer)


@app_views.route('/places/<place_id>/reviews',
                 methods=['POST'], strict_slashes=False)
def create_review():
    """ request to create a review """
    new_review = request.get_json(silent=True)
    if new_review is None:
        return "Not a JSON", 400
    one_place = storage.get(Place, place_id)
    if one_place is None:
        abort(404)
    if 'user_id' not in new_review:
        return ("Missing user_id", 400)
    review_user_id = new_review.get('user_id')
    review_user_exist = storage.get(Review, review_user_id)
    if review_user_exist is None:
        abort(404)
    if 'text' not in new_review:
        return ("Missing text", 400)
    review_created = Review(**new_review)
    storage.new(review_created)
    storage.save()
    return jsonify(review_created.to_dict()), 201


@app_views.route('/reviews/<review_id>',
                 methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    """ updates the review object """
    upd_review = request.get_json(silent=True)
    if upd_review is None:
        return "Not a JSON", 400
    review_to_update = storage.get(Review, review_id)
    if review_to_update is None:
        abort(404)
    list_ignore = ['id', 'updated_at', 'created_at', 'user_id', 'place_id']
    for key, value in upd_review.items():
        if key not in list_ignore:
            setattr(review_to_update, key, value)
    storage.save()
    return jsonify(review_to_update.to_dict())
