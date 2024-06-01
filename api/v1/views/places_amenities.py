#!/usr/bin/python3
""" Create a new view for the link between Place
objects and Amenity objects that handles all
efault RESTFul API actions:
"""
from flask import jsonify, abort
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from models.place import Place
from os import getenv


@app_views.route('/places/<place_id>/amenities', methods=['GET'],
                 strict_slashes=False)
def get_amenities(place_id):
    place = storage.get(Place, place_id)
    if place:
        if getenv('HBNB_TYPE_STORAGE') == 'db':
            amenities = [amenity.to_dict() for amenity in place.amenities]
        else:
            amenities = [storage.get(Amenity, amenity_id).to_dict()
                         for amenity_id in place.amenity_ids]
        return jsonify(amenities)
    abort(404)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_amenity(place_id, amenity_id):
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)
    if place and amenity:
        if getenv('HBNB_TYPE_STORAGE') == 'db':
            if amenity not in place.amenities:
                abort(404)
            place.amenities.remove(amenity)
        else:
            if amenity_id not in place.amenity_ids:
                abort(404)
            place.amenity_ids.remove(amenity_id)
        place.save()
        return jsonify({}), 200
    abort(404)

@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['POST'], strict_slashes=False)
def link_amenity(place_id, amenity_id):
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)
    if place and amenity:
        if getenv('HBNB_TYPE_STORAGE') == 'db':
            if amenity in place.amenities:
                return jsonify(amenity.to_dict()), 200
            place.amenities.append(amenity)
        else:
            if amenity_id in place.amenity_ids:
                return jsonify(amenity.to_dict()), 200
            place.amenity_ids.append(amenity_id)
        place.save()
        return jsonify(amenity.to_dict()), 201
    abort(404)
