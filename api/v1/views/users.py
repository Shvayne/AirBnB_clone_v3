#!/usr/bin/python3
"""This script contains an app view for User objects"""
from flask import abort, jsonify, request
from api.v1.views import app_views
from models import storage
from models.user import User

@app_views.route("/users", methods=['GET', 'POST'], strict_slashes=False)
@app_views.route("/users/<user_id>", methods=['GET', 'DELETE', 'PUT'],strict_slashes=False)
def get_users(user_id=None):
    """
        Retrieves the list of all User objects: GET /api/v1/users
        If the user_id is not linked to any User object, raise a 404 error
        deletes a user object
    """
    if not user_id:
        if request.method == 'GET':
            users = storage.all(User).values()
            users_list = [user.to_dict() for user in users]
            return jsonify(users_list)
        if request.method == 'POST':
            if not request.get_json():
                abort(400, description="Not a JSON")
            if 'email' not in request.get_json():
                abort(400, description="Missing email")
            if 'password' not in request.get_json():
                abort(400, description="Missing password")
            user_data = request.get_json()
            new = User(**user_data)
            new.save()
            return jsonify(new.to_dict()), 201
    # /users/<user_id>
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    if request.method == 'GET':
        return jsonify(user.to_dict())
    if request.method == 'DELETE':
        storage.delete(user)
        storage.save()
        return jsonify({}), 200
    if request.method == 'PUT':
        if not request.get_json():
            abort(400, description="Not a JSON")
        ignore = ["id", "email", "created_at", "updated_at"]
        user_data = request.get_json()
        for key, value in user_data.items():
            if key not in ignore:
                setattr(user, key, value)
        storage.save()
        return jsonify(user.to_dict()), 200
        