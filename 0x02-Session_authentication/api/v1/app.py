#!/usr/bin/env python3
"""
Route module for the API
"""
from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request, g
from flask_cors import (CORS, cross_origin)
from api.v1.auth.auth import Auth
from api.v1.auth.basic_auth import BasicAuth
from api.v1.auth.session_auth import SessionAuth
import os

app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

if getenv("AUTH_TYPE") == "basic_auth":
    auth = BasicAuth()
elif getenv("AUTH_TYPE") == "session_auth":
    auth = SessionAuth()
else:
    auth = Auth()


@app.before_request
def before_request_handler():
    """
    Method to filter each request
    """
    global auth
    if auth is None:
        return

    exempt_paths = ['/api/v1/status/',
                    '/api/v1/unauthorized/',
                    '/api/v1/forbidden/',
                    '/api/v1/auth_session/login/'
                    ]

    if auth.require_auth(request.path, exempt_paths):
        return

    if auth.authorization_header(request) is None and auth.session_cookie(
            request) is None:
        abort(401)

    current_user = auth.current_user(request)
    if current_user is None:
        abort(403)

    g.current_user = current_user


@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found handler
    """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def unauthorized(error) -> str:
    """
    Unauthorized error handler
    """
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden_error(error):
    """
    Forbidden error handler
    """
    response = jsonify({"error": "Forbidden"})
    response.status_code = 403
    return response


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
