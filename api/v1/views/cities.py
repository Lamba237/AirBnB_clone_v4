#!/usr/bin/python3
""" a new view for City objects that handles all
default RESTFul API actions
"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def get_cities(state_id):
    state = storage.get(State, state_id)
    if state:
        return jsonify([city.to_dict() for city in state.cities])
    abort(404)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city(city_id):
    city = storage.get(City, city_id)
    if city:
        return jsonify(city.to_dict())
    abort(404)


@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    city = storage.get(City, city_id)
    if city:
        storage.delete(city)
        storage.save()
        return jsonify({}), 200
    abort(404)


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def create_city(state_id):
    state = storage.get(State, state_id)
    if state:
        if not request.get_json():
            abort(400, description="Not a JSON")
        if 'name' not in request.get_json():
            abort(400, description="Missing name")
        city = City(state_id=state_id, **request.get_json())
        city.save()
        return jsonify(city.to_dict()), 201
    abort(404)


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    city = storage.get(City, city_id)
    if city:
        if not request.get_json():
            abort(400, description="Not a JSON")
        for key, value in request.get_json().items():
            if key not in ['id', 'state_id', 'created_at', 'updated_at']:
                setattr(city, key, value)
        city.save()
        return jsonify(city.to_dict()), 200
    abort(404)
