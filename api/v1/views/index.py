#!/usr/bin/python3
"""routing paths"""
from api.v1.views import app_views
from flask import jsonify

@app_views.route("/status", strict_slashes=False)
def return_status():
    """returns the status of the api when called"""
    return jsonify({"status": "OK"})