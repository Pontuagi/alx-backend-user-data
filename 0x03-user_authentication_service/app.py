#!/usr/bin/env python3

"""
Flask app module
"""

from flask import Flask, jsonify, request
from auth import Auth
from db import DB

app = Flask(__name__)
AUTH = Auth()


@app.route("/")
def welcome():
    """ Welcome message

    return:
        - json payload
    """
    message = {"message": "Bienvenue"}
    return jsonify(message)


@app.route("/users", methods=["POST"])
def register_user():
    try:
        email = request.form.get("email")
        password = request.form.get("password")

        # Check if the user already exists
        existing_user = AUTH._find_user_by(email=email)

        # If user exists, return a JSON payload with an error message
        return jsonify({"message": "email already registered"}), 400

    except ValueError:
        # User does not exist, proceed with registration
        new_user = AUTH.register_user(email, password)

        # Return a JSON payload with the registered email and success message
        return jsonify({"email": new_user.email, "message": "user created"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
