#!/usr/bin/python3
"""routing paths"""
from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from models.user import User

@app_views.route("/status", strict_slashes=False)
def get_status():
    """returns the status of the api when called"""
    return jsonify({"status": "OK"})

@app_views.route("/stats", strict_slashes=False)
def get_stats():
    """retrieve the number of each obj by type"""
    classes = {
        "states": State, "cities": City, "amenities": Amenity, "places": Place, "reviews": Review, "users": User
    }
    stats = {key: storage.count(value) for key, value in classes.items()}
    return jsonify(stats)