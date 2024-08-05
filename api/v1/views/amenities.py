#!/usr/bin/python3
"""script for an app view for amenity obejcts"""
from flask import abort, jsonify, request
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity

@app_views.route("/amenities", methods=['GET', 'POST'], strict_slashes=False)
@app_views.route("/amenities/<amenity_id>", method=['GET', 'DELETE', 'PUT'], strict_slashes=False)
def get_amenities(amenity_id=None):
    """
    Returns a list of amenity objects or if a PUT rqt is
    encountered, create a new amenity object.
    """
    if not amenity_id:
        if request.method == 'GET':
            amenities = storage.all(Amenity).values()
            amenities_list = [amenity.to_dict() for amenity in amenities]
            return jsonify(amenities_list)
        if request.method == 'POST':
            if not request.get_json():
                abort(400, description="Not a JSON")
            if 'name' not in request.get_json():
                abort(400, description="Missing name")
            amenity_data = request.get_json()
            new = Amenity(**amenity_data)
            new.save()
            return jsonify(new.to_ict()), 201
        
        # /amenities/<amenity_id>
        amenity = storage.get(Amenity, amenity_id)
        if not amenity:
            abort(404)
        if request.method == 'GET':
            return jsonify(amenity.to_dict())
        if request.method == 'DELETE':
            storage.delete(amenity)
            storage.save()
            return jsonify({}), 200
        if request.method == 'PUT':
            if not request.get_json():
                abort(400, description="Not a JSON")
            ignore = ["id", "created_at", "updated_at"]
            amenity_data = request.get_json()
            for key, value in amenity_data.items():
                if key not in ignore:
                    setattr(amenity, key, value)
            storage.save()
            return jsonify(amenity.to_dict()), 200
        