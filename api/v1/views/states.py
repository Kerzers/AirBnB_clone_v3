#!/usr/bin/python3
"""comment for file"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def listofstatus():
    """comment for func"""
    ob = storage.all('State')
    ll = []
    for state in ob.values():
        ll.append(state.to_dict())
    return jsonify(ll)


@app_views.route('/states/<string:state_id>',
                 methods=['GET'], strict_slashes=False)
def StatusWithId(state_id):
    """gets obj with id"""
    ob = storage.all('State')
    for x in ob.values():
        if x.id == state_id:
            return jsonify(x.to_dict())
    abort(404)


@app_views.route('/states/<string:state_id>',
                 methods=['DELETE'], strict_slashes=False)
def DeleteObj(state_id):
    """deletes obj"""
    x = storage.get(State, state_id)
    if x is None:
        abort(404)
    storage.delete(x)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/<string:state_id>', methods=['PUT'],
                 strict_slashes=False)
def putinV(state_id):
    '''vladimir'''
    try:
        response = request.get_json()
    except ex:
        abort(400, {'Not a JSON'})
    if response.get('name') is None:
        abort(400, {'Missing name'})
    stateObject = storage.get(State, state_id)
    if stateObject is None:
        abort(404)
    ignoreKeys = ['id', 'created_at', 'updated_at']
    for key, val in response.items():
        if key not in ignoreKeys:
            setattr(stateObject, key, val)
    storage.save()
    return jsonify(stateObject.to_dict()), '200'


@app_views.route('/states/', methods=['POST'],
                 strict_slashes=False)
def posting():
    '''Creates a State'''
    try:
        response = request.get_json()
    except ex:
        abort(400, {'Not a JSON'})
    if response.get('name') is None:
        abort(400, {'Missing name'})
    stateObject = State(name=response['name'])
    storage.new(stateObject)
    storage.save()
    return jsonify(stateObject.to_dict()), '201'
