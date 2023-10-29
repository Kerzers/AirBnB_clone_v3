#!/usr/bin/python3
"""create a route /cities on the object app_views that returns a JSON"""
from api.v1.views import app_views
from models import storage
from models.state import City, State, Place
from flask import jsonify, abort
from flask import request


@app_views.route("/cities/<city_id>/places", methods=["GET"],
                 strict_slashes=False)
def palces(city_id):
    list_places = []
    city = storage.get(City, places_id)
    if not city:
        abort(404)
    for place in city.places:
        list_places.append(place.to_dict())

    return jsonify(list_places)


@app_views.route("/places/<place_id>", methods=["GET"], strict_slashes=False)
def place_id(place_id):
    place = storage.get(Place, places_id)
    if not place:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route("/places/<id>", methods=["DELETE"], strict_slashes=False)
def del_place(places_id):
    place = storage.get(Place, places_id)
    if not place:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route("/cities/<city_id>/places", methods=["POST"],
                 strict_slashes=False)
def create_place(city_id):
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    response = request.get_json()
    if response is None:
        abort(400, description="Not a JSON")

    if 'name' not in response:
        abort(400, description="Missing name")

    new_place = City(name=response['name'])
    new_place.city_id = city.id
    new_placee.save()

    return jsonify(new_place.to_dict()), 201


@app_views.route("/places/<place_id>", methods=["PUT"], strict_slashes=False)
def update_city(place_id):
    place = storage.get(Place, place_id)
    response = request.get_json()
    if not place:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    not_in = ['id', 'created_at', 'updated_at', 'city_id']

    for key, value in response.items():
        if key not in not_in:
            setattr(place, key, value)
    storage.save()
    return jsonify(place.to_dict()), 200
