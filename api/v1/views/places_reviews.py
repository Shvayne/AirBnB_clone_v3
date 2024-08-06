#!/usr/bin/python3
"""App views for reviews on places"""
from flask import abort, jsonify, request
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.user import User
from models.review import Review

@app_views.route("/places/<place_id>/reviews", methods=['GET', 'POST'], strict_slashes=False)
def add_get_reviews(place_id):
    """Get a list of all review objects or create a new review"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    if request.method == 'GET':
        reviews = [review.to_dict() for review in place.reviews]
        return jsonify(reviews)
    if request.method == 'POST':
        if not request.get_json():
            abort(400, description="Not a JSON")
        if 'user_id' not in request.get_json():
            abort(400, description="Missing user_id")
        if 'text' not in request.get_json():
            abort(400, description="Missing text")
        review_data = request.get_json()
        user = storage.get(User, review_data["user_id"])
        if not user:
            abort(404)
        new = Review(**review_data)
        new.place_id = place_id
        new.save()
        return jsonify(new.to_dict()), 201


@app_views.route(
        "/reviews/<review_id>", methods=['GET', 'DELETE', 'PUT'],
        strict_slashes=False)
def get_delete_update_review(review_id):
    """
    Retrieves, Deletes or Updates a specific Review object
    """
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    if request.method == 'GET':
        return jsonify(review.to_dict())

    if request.method == 'DELETE':
        storage.delete(review)
        storage.save()
        return jsonify({}), 200

    if request.method == 'PUT':
        if not request.get_json():
            abort(400, description="Not a JSON")
        ignore = ["id", "user_id", "place_id", "created_at", "updated_at"]
        review_data = request.get_json()
        for key, value in review_data.items():
            if key not in ignore:
                setattr(review, key, value)
        storage.save()
        return jsonify(review.to_dict()), 201