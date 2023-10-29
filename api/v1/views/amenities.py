#!/usr/bin/python3
"""create a route /status on the object app_views that returns a JSON"""
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from flask import jsonify, abort
from flask import request


@app_views.route("/amenities", methods=["GET"], strict_slashes=False)
def amenities():
    dict_amenities = storage.all(Amenity)
    list_amenities = []
    for amenity in dict_amenities.values():
        list_amenities.append(amenity.to_dict())
    return jsonify(list_amenities)


@app_views.route("/amenities/<id>", methods=["GET"], strict_slashes=False)
def amenities_id(id):
    amenity = storage.get(Amenity, id)
    if not amenity:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route("/amenities/<id>", methods=["DELETE"], strict_slashes=False)
def del_amenity(id):
    amenity = storage.get(Amenity, id)
    if not amenity:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return jsonify({}), 200


@app_views.route("/amenities", methods=["POST"], strict_slashes=False)
def create_amenity():

    response = request.get_json()
    if not response:
        abort(400, description="Not a JSON")

    if 'name' not in response:
        abort(400, description="Missing name")

    new_amenity = Amenity(name=response['name'])
    new_amenity.save()

    return jsonify(new_amenity.to_dict()), 201


@app_views.route("/amenities/<id>", methods=["PUT"], strict_slashes=False)
def update_amenity(id):
    amenity = storage.get(Amenity, id)
    response = request.get_json()

    if not amenity:
        abort(404)
    if not response:
        abort(400, description="Not a JSON")

    not_in = ['id', 'create_at', 'updated_at']
    for key, value in response.items():
        if key not in not_in:
            setattr(amenity, key, value)

    storage.save()

    return jsonify(amenity.to_dict()), 200
