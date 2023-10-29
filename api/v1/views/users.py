#!/usr/bin/python3
"""create a route /status on the object app_views that returns a JSON"""
from api.v1.views import app_views
from models import storage
from models.user import User
from flask import jsonify, abort
from flask import request


@app_views.route("/users", methods=["GET"], strict_slashes=False)
def users():
    dict_users = storage.all(User)
    list_users = []
    for user in dict_users.values():
        list_users.append(user.to_dict())
    return jsonify(list_users)


@app_views.route("/users/<id>", methods=["GET"], strict_slashes=False)
def users_id(id):
    user = storage.get(User, id)
    if not user:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route("/users/<id>", methods=["DELETE"], strict_slashes=False)
def del_user(id):
    user = storage.get(User, id)
    if not user:
        abort(404)
    storage.delete(user)
    storage.save()
    return jsonify({}), 200


@app_views.route("/users", methods=["POST"], strict_slashes=False)
def create_user():

    response = request.get_json()
    if not response:
        abort(400, description="Not a JSON")

    if 'email' not in response:
        abort(400, description="Missing email")
    if 'password' not in response:
        abort(400, description="Missing password")

    new_user = User(email=response['email'], password=response['password'])
    new_user.save()

    return jsonify(new_user.to_dict()), 201


@app_views.route("/users/<id>", methods=["PUT"], strict_slashes=False)
def update_user(id):
    user = storage.get(User, id)
    response = request.get_json()

    if not user:
        abort(404)
    if not response:
        abort(400, description="Not a JSON")

    not_in = ['id', 'email', 'create_at', 'updated_at']
    for key, value in response.items():
        if key not in not_in:
            setattr(user, key, value)

    storage.save()

    return jsonify(user.to_dict()), 200
