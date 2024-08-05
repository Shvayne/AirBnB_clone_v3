#!/usr/bin/python3
"""App view for the Place objects"""
from flask import abort, jsonify, request
from api.v1.views import app_views
from models import storage
from models.city import City
from models.place import Place
from models.user import User

@app_views.route("/cities/<city_id>/places", methods=['GET', 'POST'], strict_slashes=False)
def add_get_places(city_id):
    """
    create or get a city obj depending on the rqst method
    """
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    if request.method == 'GET':
        places = [place.to_dict() for place in city.places]
        return jsonify(places)

    if request.method == 'POST':
        if not request.get_json():
            abort(400, description="Not a JSON")
        if 'name' not in request.get_json():
            abort(400, description="Missing name")
        if 'user_id' not in request.get_json():
            abort(400, description="Missing user_id")
        place_data = request.get_json()
        user = storage.get(User, place_data["user_id"])
        if not user:
            abort(404)
        new = Place(**place_data)
        new.city_id = city_id
        new.save()
        return jsonify(new.to_dict()), 201


@app_views.route(
        "/places/<place_id>", methods=['GET', 'DELETE', 'PUT'],
        strict_slashes=False)
def get_delete_update_place(place_id):
    """
    Retrieves, Deletes or Updates Place objects
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    if request.method == 'GET':
        return jsonify(place.to_dict())

    if request.method == 'DELETE':
        storage.delete(place)
        storage.save()
        return jsonify({}), 200

    if request.method == 'PUT':
        if not request.get_json():
            abort(400, description="Not a JSON")
        ignore = ["id", "user_id", "city_id", "created_at", "updated_at"]
        place_data = request.get_json()
        for key, value in place_data.items():
            if key not in ignore:
                setattr(place, key, value)
        storage.save()
        return jsonify(place.to_dict()), 200