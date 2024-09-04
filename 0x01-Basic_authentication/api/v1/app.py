#!/usr/bin/env python3
"""
Route module for the API
"""
import logging
from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import (CORS, cross_origin)
import os

logger = logging.getLogger('user_data')
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler('api.log')
file_handler.setFormatter('%(message)s')
logger.addHandler(file_handler)

app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
auth = os.getenv('AUTH_TYPE')

if auth:
    from api.v1.auth.auth import Auth
    auth = Auth()


@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found handler
    """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def unauthorized(error) -> str:
    """ Unauthorized handler
    """
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden(error) -> str:
    """ Forbidden handler
    """
    return jsonify({"error": "Forbidden"}), 403


@app.before_request
def filter() -> str:
    """ Filter request
    """
    urls = ['/api/v1/status/', '/api/v1/unauthorized/', '/api/v1/forbidden/']
    if auth is None:
        pass

    if auth.require_auth(request.path, urls) is True:
        pass

    if auth.authorization_header(request) is None:
        logger.debug(request)
        abort(401)

    if auth.current_user(request) is None:
        logger.debug(request)
        abort(403)


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
