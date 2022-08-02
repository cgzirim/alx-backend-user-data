#!/usr/bin/env python3
"""Basic Flask app."""
from auth import Auth
from flask import Flask, jsonify
from flask import request, abort


AUTH = Auth()
app = Flask(__name__)


@app.route('/', methods=['GET'], strict_slashes=False)
def hello() -> str:
    """GET /
    Returns JSON payload.
    """
    return jsonify({'message': 'Bienvenue'})


@app.route('/users', methods=['POST'], strict_slashes=False)
def users():
    """POST /users
    Registers a user and returns a JSON payload.
    """
    email = request.form.get('email')
    password = request.form.get('password')

    if not email or not password:
        abort(400)

    try:
        AUTH.register_user(email=email, password=password)
        return jsonify({
            "email": "{}".format(email),
            "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login():
    """POST /sessions
    Validates email and password in POST request.
    Return:
        - Error code 401 if email doesn't exist or the password isn't valid
        - JSON payload with a cookie attached to the response.
    """
    email = request.form.get('email')
    password = request.form.get('password')
    if email is None or password is None:
        abort(401)

    if AUTH.valid_login(email, password) is False:
        abort(401)

    session_id = AUTH.create_session(email)

    # Set cookie to the response
    response = jsonify({"email": "{}".format(email), "message": "logged in"})
    response.set_cookie("session_id", session_id)

    return response


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000", debug=True)
