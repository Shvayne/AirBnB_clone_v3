#!/usr/bin/python3
"""create v1 of the app"""
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
from os import getenv
from flask_cors import CORS


app = Flask(__name__)
app.register_blueprint(app_views)
cors = CORS(app, resources={
    r"api/v1/*": {
        "origins": "0.0.0.0"
    }
})

@app.teardown_appcontext
def close_session(self):
    """close the current sqlalchecmy session"""
    storage.close()

if __name__ == "__main__":
    host = getenv("HBNB_API_HOST") if getenv("HBNB_API_HOST") else "0.0.0.0"
    port = getenv("HBNB_API_PORT") if getenv("HBNB_API_PORT") else 5000
    app.run(host=host, port=port, threaded=True)
