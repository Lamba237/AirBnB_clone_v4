#!/usr/bin/python3
"""
This module starts a Flask web application.

It includes routes for handling all default RESTful API actions.
"""

from api.v1.views import app_views
from flask import Flask, jsonify
from flask_cors import CORS
from models import storage
from os import getenv

app = Flask(__name__)
app.register_blueprint(app_views)
cors = CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def tearDown(self):
    """
    Close the database storage on Teardown.

    This function is called after each request, ensuring that the database
    connection is closed and resources are freed up.
    """
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """
    Handle 404 errors by returning a JSON response.

    Args:
        error (Exception): The error that caused the 404 response.

    Returns:
        Response: A JSON response with a 404 status code and an error message.
    """
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    # Get the host and port from the environment, or use defaults
    HBNB_API_HOST = getenv("HBNB_API_HOST", '0.0.0.0')
    HBNB_API_PORT = int(getenv("HBNB_API_PORT", 5000))

    # Start the Flask application
    app.run(host=HBNB_API_HOST, port=HBNB_API_PORT, threaded=True)
