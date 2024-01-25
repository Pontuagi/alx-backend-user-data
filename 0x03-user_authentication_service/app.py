#!/usr/bin/env python3

"""
Flask app module
"""

from flask import Flask, jsonify, request, Response
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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
