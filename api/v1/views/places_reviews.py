#!/usr/bin/python3
"""create a route /review on the object app_views that returns a JSON"""
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.review import Review
from models.user import User
from flask import jsonify, abort, request


@app_views.route("/places/<place_id>/reviews", methods=["GET"],
                 strict_slashes=False)
def reviews(place_id):
    list_reviews = []
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    for review in place.reviews:
        list_reviews.append(review.to_dict())

    return jsonify(list_reviews)


@app_views.route("/reviews/<review_id>", methods=["GET"], strict_slashes=False)
def review_id(review_id):
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route("/reviews/<review_id>", methods=["DELETE"],
                 strict_slashes=False)
def del_review(review_id):
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    storage.delete(review)
    storage.save()
    return jsonify({}), 200


@app_views.route("/places/<place_id>/reviews", methods=["POST"],
                 strict_slashes=False)
def create_review(place_id):
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    response = request.get_json()
    if response is None:
        abort(400, description="Not a JSON")

    if 'user_id' not in response.keys():
        abort(400, description="Missing user_id")

    if storage.get(User, response['user_id']) is None:
        abort(404)

    if 'text' not in response.keys():
        abort(400, description="Missing text")

    new_review = Review(**response)
    new_review.place_id = place.id
    new_review.save()

    return jsonify(new_review.to_dict()), 201


@app_views.route("/reviews/<review_id>", methods=["PUT"], strict_slashes=False)
def update_review(review_id):
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)

    response = request.get_json()
    if response is None:
        abort(400, description="Not a JSON")

    keys_to_ignore = ['id', 'place_id', 'created_at', 'updated_at', 'user_id']

    for key, value in response.items():
        if key not in keys_to_ignore:
            setattr(review, key, value)

    storage.save()
    return jsonify(review.to_dict()), 200
