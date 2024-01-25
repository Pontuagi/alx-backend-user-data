#!/usr/bin/env python3

"""
Flask app module
"""

from flask import Flask, jsonify, request, Response, abort
from flask import make_response
from auth import Auth

app = Flask(__name__)
AUTH = Auth()


@app.route("/", methods=["GET"], strict_slashes=False)
def welcome() -> Response:
    """ Welcome message

    return:
        - json payload
    """
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"], strict_slashes=False)
def register_user() -> Response:
    """
    Register user a new user
    """
    email = request.form.get('email')
    password = request.form.get('password')

    try:
        AUTH.register_user(email, password)
        return jsonify({"email": email, "message": "user created"})

    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route("/sessions", methods=["POST"], strict_slashes=False)
def login():
    """
    Login session
    """
    email = request.form.get("email")
    password = request.form.get("password")

    if AUTH.valid_login(email, password):
        # User is authenticated
        session_id = AUTH.create_session(email)

        # Set the session ID as a cookie
        response = make_response(jsonify(
            {"email": email, "message": "logged in"}))
        response.set_cookie("session_id", session_id)

        return response
    else:
        # Invalid login information
        abort(401)


@app.route("/sessions", methods=["DELETE"], strict_slashes=False)
def logout():
    """
    Logout Session
    """
    session_id = request.cookies.get("session_id")

    if session_id is None:
        abort(403)

    try:
        user = AUTH.get_user_from_session_id(session_id)
        if user:
            AUTH.destroy_session(user.id)
            return redirect("/")
        else:
            abort(403)
    except Exception as e:
        abort(403)


@app.route("/profile", methods=["GET"], strict_slashes=False)
def profile():
    """
    Get user profile
    """
    session_id = request.cookies.get("session_id")

    if session_id is None:
        abort(403)

    try:
        user = AUTH.get_user_from_session_id(session_id)

        if user:
            return jsonify({"email": user.email}), 200
        else:
            abort(403)
    except Exception as e:
        abort(403)


@app.route("/reset_password", methods=["POST"], strict_slashes=False)
def get_reset_password_token():
    """
    Get reset password token for a user.
    """
    email = request.form.get("email")

    if not email:
        abort(403)

    try:
        reset_token = AUTH.get_reset_password_token(email)
        return jsonify({"email": email, "reset_token": reset_token}), 200
    except ValueError:
        abort(403)


@app.route("/reset_password", methods=["PUT"], strict_slashes=False)
def update_password():
    """
    Update user's password using reset_token.
    """
    try:
        email = request.form.get("email")
        reset_token = request.form.get("reset_token")
        new_password = request.form.get("new_password")

        AUTH.update_password(reset_token, new_password)

        return jsonify({"email": email, "message": "Password updated"}), 200

    except ValueError:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
