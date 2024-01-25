#!/usr/bin/env python3

"""
Flask app module
"""

from flask import Flask, jsonify, request
from auth import Auth

app = Flask(__name__)
AUTH = Auth()


@app.route("/", methods=["GET"])
def welcome():
    """ Welcome message

    return:
        - json payload
    """
    message = {"message": "Bienvenue"}
    return jsonify(message)


@app.route("/users", methods=["POST"])
def register_user():
    """
    Register user a new user
    """
    try:
        email = request.form.get("email")
        password = request.form.get("password")
        new_user = AUTH.register_user(email, password)
        return jsonify({"email": new_user.email, "message": "user created"})

    except ValueError:
        return jsonify({"message": "email already registered"}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
