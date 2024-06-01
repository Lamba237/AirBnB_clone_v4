#!/usr/bin/python3
""" This module creates a new view for Review object
that handles all default RESTFul API actions
"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.review import Review
from models.place import Place
from models.user import User


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def get_reviews(place_id):
    place = storage.get(Place, place_id)
    if place:
        return jsonify([review.to_dict() for review in place.reviews])
    abort(404)


@app_views.route('/reviews/<review_id>', methods=['GET'],
                 strict_slashes=False)
def get_review(review_id):
    review = storage.get(Review, review_id)
    if review:
        return jsonify(review.to_dict())
    abort(404)


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    review = storage.get(Review, review_id)
    if review:
        storage.delete(review)
        storage.save()
        return jsonify({}), 200
    abort(404)


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def create_review(place_id):
    place = storage.get(Place, place_id)
    if place:
        if not request.get_json():
            abort(400, description="Not a JSON")
        if 'user_id' not in request.get_json():
            abort(400, description="Missing user_id")
        user = storage.get(User, request.get_json()['user_id'])
        if not user:
            abort(404)
        if 'text' not in request.get_json():
            abort(400, description="Missing text")
        review = Review(place_id=place_id, **request.get_json())
        review.save()
        return jsonify(review.to_dict()), 201
    abort(404)


@app_views.route('/reviews/<review_id>', methods=['PUT'],
                 strict_slashes=False)
def update_review(review_id):
    review = storage.get(Review, review_id)
    if review:
        if not request.get_json():
            abort(400, description="Not a JSON")
        for key, value in request.get_json().items():
            if key not in ['id', 'user_id', 'place_id',
                           'created_at', 'updated_at']:
                setattr(review, key, value)
        review.save()
        return jsonify(review.to_dict()), 200
    abort(404)
