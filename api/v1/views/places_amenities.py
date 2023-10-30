#!/usr/bin/python3
"""create a route /amenities on the object app_views that returns a JSON"""
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.amenity import Amenity
from flask import jsonify, abort, request
from os import getenv


@app_views.route("/places/<place_id>/amenities", methods=["GET"],
                 strict_slashes=False)
def amenities(place_id):
    list_amenities = []
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if getenv("HBNB_TYPE_STORAGE") == "db":
        for amenity in place.amenities:
            list_amenities.append(amenity.to_dict())
    else:
        for amenity_id in place.amenity_ids:
            amenity = storage.get(Amenity, amenity_id)
            list_amenities.append(amenity.to_dict())

    return jsonify(list_amenities)


@app_views.route("/places/<place_id>/amenities/<amenity_id>",
                 methods=["DELETE"], strict_slashes=False)
def place_amenity_id(place_id, amenity_id):
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)
    if place is None:
        abort(404)
    if amenity is None:
        abort(404)
    if getenv("HBNB_TYPE_STORAGE") == "db":
        if amenity in place.amenities:
            place.amenities.remove(amenity)
        else:
            abort(404)
    else:
        if amenity_id in place.amenity_ids:
            place.amenities.remove(amenity_ids)
        else:
            abort(404)

    storage.save()
    return jsonify({}), 200


@app_views.route("/places/<place_id>/amenities/<amenity_id>",
                 methods=["POST"], strict_slashes=False)
def create_place_amenity(place_id, amenity_id):

    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)
    if place is None:
        abort(404)
    if amenity is None:
        abort(404)
    if getenv("HBNB_TYPE_STORAGE") == "db":
        if amenity in place.amenities:
            return jasonify(amenity.to_dict()), 200
        else:
            place.amenities.append(amenity)
    else:
        if amenity_id in place.amenity_ids:
            return jasonify(amenity.to_dict()), 200
        else:
            place.amenity_ids.append(amenity_id)

    storage.save()
    return jsonify(amenity.to_dict()), 201
