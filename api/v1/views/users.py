#!/usr/bin/python3
""" Creates new view for uder object that handles
All default RESTful api calls
"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    return jsonify([user.to_dict() for user in storage.all(User).values()])


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user(user_id):
    user = storage.get(User, user_id)
    if user:
        return jsonify(user.to_dict())
    abort(404)


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    user = storage.get(User, user_id)
    if user:
        storage.delete(user)
        storage.save()
        return jsonify({}), 200
    abort(404)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    if not request.get_json():
        abort(400, description="Not a JSON")
    if 'email' not in request.get_json():
        abort(400, description="Missing email")
    if 'password' not in request.get_json():
        abort(400, description="Missing password")
    user = User(**request.get_json())
    user.save()
    return jsonify(user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    user = storage.get(User, user_id)
    if user:
        if not request.get_json():
            abort(400, description="Not a JSON")
        for key, value in request.get_json().items():
            if key not in ['id', 'email', 'created_at', 'updated_at']:
                setattr(user, key, value)
        user.save()
        return jsonify(user.to_dict()), 200
    abort(404)
