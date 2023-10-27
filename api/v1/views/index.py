#!/usr/bin/python3
"""create a route /status on the object app_views that returns a JSON"""
import json
from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User

classes = {"Amenity": Amenity, "BaseModel": BaseModel, "City": City,
           "Place": Place, "Review": Review, "State": State, "User": User}


@app_views.route("/status", methods=["GET"], strict_slashes=False)
def status():
    return jsonify({"status": "OK"})


@app_views.route("/stats", methods=["GET"], strict_slashes=False)
def stats():
    result_dict = {
            "amenities": storage.count(Amenity),
            "cities": storage.count(City),
            "places": storage.count(Place),
            "reviews": storage.count(Review),
            "states": storage.count(State),
            "users": storage.count(User)
            }
    json_data = json.dumps(result_dict, indent=4)
    return json_data
