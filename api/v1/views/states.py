#!/usr/bin/python3
"""create a route /status on the object app_views that returns a JSON"""
from api.v1.views import app_views
from models import storage
from models.state import State
from flask import jsonify, abort
from flask import request


@app_views.route("/states", methods=["GET"], strict_slashes=False)
def states():
    dict_states = storage.all(State)
    list_states = []
    for state in dict_states.values():
        list_states.append(state.to_dict())
    return jsonify(list_states)


@app_views.route("/states/<id>", methods=["GET"], strict_slashes=False)
def states_id(id):
    state = storage.get(State, id)
    if not state:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route("/states/<id>", methods=["DELETE"], strict_slashes=False)
def del_state(id):
    state = storage.get(State, id)
    if not state:
        abort(404)
    storage.delete(state)
    storage.save()
    return jsonify({}), 200


@app_views.route("/states", methods=["POST"], strict_slashes=False)
def create_state():

    response = request.get_json()
    if not response:
        abort(400, description="Not a JSON")

    if 'name' not in response:
        abort(400, description="Missing name")

    new_state = State(name=response['name'])
    new_state.save()

    return jsonify(new_state.to_dict()), 201


@app_views.route("/states/<id>", methods=["PUT"], strict_slashes=False)
def update_state(id):
    state = storage.get(State, id)
    response = request.get_json()

    if not state:
        abort(404)
    if not response:
        abort(400, description="Not a JSON")

    not_in = ['id', 'create_at', 'updated_at']
    for key, value in response.items():
        if key not in not_in:
            setattr(state, key, value)

    storage.save()

    return jsonify(state.to_dict()), 200
