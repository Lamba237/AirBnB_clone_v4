#!/usr/bin/python3
""" Creates a new view for Place object that handles
all default Restful Api actions
"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.city import City
from models.user import User


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_places(city_id):
    city = storage.get(City, city_id)
    if city:
        return jsonify([place.to_dict() for place in city.places])
    abort(404)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    place = storage.get(Place, place_id)
    if place:
        return jsonify(place.to_dict())
    abort(404)


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    place = storage.get(Place, place_id)
    if place:
        storage.delete(place)
        storage.save()
        return jsonify({}), 200
    abort(404)


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    city = storage.get(City, city_id)
    if city:
        if not request.get_json():
            abort(400, description="Not a JSON")
        if 'user_id' not in request.get_json():
            abort(400, description="Missing user_id")
        user = storage.get(User, request.get_json()['user_id'])
        if not user:
            abort(404)
        if 'name' not in request.get_json():
            abort(400, description="Missing name")
        place = Place(city_id=city_id, **request.get_json())
        place.save()
        return jsonify(place.to_dict()), 201
    abort(404)


@app_views.route('/places/<place_id>', methods=['PUT'],
                 strict_slashes=False)
def update_place(place_id):
    place = storage.get(Place, place_id)
    if place:
        if not request.get_json():
            abort(400, description="Not a JSON")
        for key, value in request.get_json().items():
            if key not in ['id', 'user_id', 'city_id',
                           'created_at', 'updated_at']:
                setattr(place, key, value)
        place.save()
        return jsonify(place.to_dict()), 200
    abort(404)
