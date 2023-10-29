#!/usr/bin/python3
"""create a route /cities on the object app_views that returns a JSON"""
from api.v1.views import app_views
from models import storage
from models.state import City, State
from flask import jsonify, abort
from flask import request


@app_views.route("/states/<id>/cities", methods=["GET"], strict_slashes=False)
def cities(id):
    list_cities = []
    state = storage.get(State, id)
    if not state:
        abort(404)
    for city in state.cities:
        list_cities.append(city.to_dict())

    return jsonify(list_cities)


@app_views.route("/cities/<id>", methods=["GET"], strict_slashes=False)
def city_id(id):
    city = storage.get(City, id)
    if not city:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route("/cities/<id>", methods=["DELETE"], strict_slashes=False)
def del_city(id):
    city = storage.get(City, id)
    if not city:
        abort(404)
    storage.delete(city)
    storage.save()
    return jsonify({}), 200


@app_views.route("/states/<state_id>/cities", methods=["POST"],
                 strict_slashes=False)
def create_city(state_id):
    state = storage.get(State, state_id)
    # print("test: ".format(state))
    if state is None:
        abort(404)

    response = request.get_json()
    if response is None:
        abort(400, description="Not a JSON")

    if 'name' not in response:
        abort(400, description="Missing name")

    new_city = City(name=response['name'])
    new_city.state_id = state.id
    # storage.save()
    new_city.save()

    return jsonify(new_city.to_dict()), 201


@app_views.route("/cities/<id>", methods=["PUT"], strict_slashes=False)
def update_city(id):
    city = storage.get(City, id)
    response = request.get_json()
    if not city:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    not_in = ['id', 'created_at', 'updated_at', 'state_id']

    for key, value in response.items():
        if key not in not_in:
            setattr(city, key, value)
    storage.save()
    return jsonify(city.to_dict()), 200