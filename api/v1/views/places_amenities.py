#!/usr/bin/python3
"""create a route /amenities on the object app_views that returns a JSON"""
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.amenity import Amenity
from flask import jsonify, abort, request
from os import getenv

@app_views.route("/places/<place_id>/amenities", methods=["GET"], strict_slashes=False)
def get_place_amenities(place_id):
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    if getenv("HBNB_TYPE_STORAGE") == "db":
        list_amenities = [amenity.to_dict() for amenity in place.amenities]
    else:
        list_amenities = []
        for amenity_id in place.amenity_ids:
            amenity = storage.get(Amenity, amenity_id)
            if amenity:
                list_amenities.append(amenity.to_dict())

    return jsonify(list_amenities)

@app_views.route("/places/<place_id>/amenities/<amenity_id>", methods=["DELETE"], strict_slashes=False)
def delete_place_amenity(place_id, amenity_id):
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)
    
    if place is None or amenity is None:
        abort(404)

    if getenv("HBNB_TYPE_STORAGE") == "db":
        if amenity not in place.amenities:
            abort(404)
        place.amenities.remove(amenity)
    else:
        if amenity_id not in place.amenity_ids:
            abort(404)
        place.amenity_ids.remove(amenity_id)

    storage.save()
    return jsonify({}), 200

@app_views.route("/places/<place_id>/amenities/<amenity_id>", methods=["POST"], strict_slashes=False)
def add_place_amenity(place_id, amenity_id):
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)
    
    if place is None or amenity is None:
        abort(404)

    if getenv("HBNB_TYPE_STORAGE") == "db":
        if amenity in place.amenities:
            return jsonify(amenity.to_dict()), 200
        place.amenities.append(amenity)
    else:
        if amenity_id in place.amenity_ids:
            return jsonify(amenity.to_dict()), 200
        place.amenity_ids.append(amenity_id)

    storage.save()
    return jsonify(amenity.to_dict()), 201
