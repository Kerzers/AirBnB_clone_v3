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
    dict_states = storage.all(State)
    for key in dict_states.keys():
        if key.split(".")[1] == id:
            return jsonify(dict_states[key].to_dict())
    abort(404)


@app_views.route("/states/<id>", methods=["DELETE"], strict_slashes=False)
def del_state(id):
    dict_states = storage.all(State)
    for v in dict_states.values():
        if v.id == id:
            storage.delete(v)
            storage.save()
            return {}
    abort(404)


@app_views.route("/states/", methods=["POST"], strict_slashes=False)
def create_state():
    try:
        response = request.get_json()
    except ValueError:
        return jsonify({"Not a JSON"}), 400
    if 'name' not in response:
        return jsonify({"Missing name"}), 400

    new_state = State(name=response['name'])
    storage.new(new_state)
    storage.save()

    return jsonify(new_state.to_dict()), 201


@app_views.route("/states/<id>", methods=["PUT"], strict_slashes=False)
def update_state(id):
    dict_states = storage.all(State)

    state = None
    for key in dict_states.keys():
        if key.split(".")[1] == id:
            state = dict_states[key]
            break

    if state is None:
        abort(404)

    try:
        response = request.get_json()
    except ValueError:
        return jsonify({"Not a JSON"}), 400

    for key, value in response.items():
        setattr(state, key, value)

    storage.save()

    return jsonify(state.to_dict()), 200
