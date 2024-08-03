#!/usr/bin/python3
"""handles all default RESTFul API actions"""
from flask import abort, jsonify, request
from api.v1.views import app_views
from models import storage
from models.state import State

@app_views.route("/states", methods=['GET'], strict_slashes=False)
@app_views.route("/states/<state_id>", methods=['GET'], strict_slashes=False)
def get_states(state_id=None):
    """Retrieve the list of all state object, if a state id is provides, get the spevific state object"""
    if not state_id:
        states = storage.all(State).values()
        states_list = [state.to_dict() for state in states]
        return jsonify(states_list)
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    return jsonify(state.to_dict())

@app_views.route("/states/<state_id>", methods=['DELETE'], strict_slashes=False)
def delete_state(state_id):
    """Deletes a State object"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    storage.delete(state)
    storage.save()
    return jsonify({}), 200

@app_views.route("/api/v1/states", method=['POST'], strict_slashes=False)
@app_views.route("/states/<state_id>", methods=['PUT'], strict_slashes=False)
def edit_state(state_id=None):
    """makes changes to a state object or creates a new State object if no id is provided"""
    if request.method == 'POST':
        if not request.get_json():
            abort(400, description="Not a JSON")
        if 'name' not in request.get_json():
            abort(400, decription="Missing name")
        state_data = request.get_json()
        new = State(**state_data)
        new.save()
        return jsonify(new.to_dict()), 201
    if request.method == 'PUT':
        if state_id:
            state = storage.get(State, state_id)
            if not state:
                abort(404)
            if not request.get_json():
                abort(400, decription="Not a JSON")
            ignore=["id", "created_at", "updated_at"]
            state_data = request.get_json()
            for key, value in state_data.items():
                if key not in ignore:
                    setattr(state, key, value)
            storage.save()
            return jsonify(state.to_dict()), 200
