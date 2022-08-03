#!/usr/bin/env python3
"""Basic Flask app."""
from auth import Auth
from flask import Flask, jsonify, redirect
from flask import request, abort


AUTH = Auth()
app = Flask(__name__)


@app.route("/", methods=["GET"], strict_slashes=False)
def hello() -> str:
    """GET /
    Returns JSON payload.
    """
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"], strict_slashes=False)
def users():
    """POST /users
    Registers a user and returns a JSON payload.
    """
    email = request.form.get("email")
    password = request.form.get("password")

    if not email or not password:
        abort(400)

    try:
        AUTH.register_user(email=email, password=password)
        return jsonify({
            "email": "{}".format(email),
            "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route("/sessions", methods=["POST"], strict_slashes=False)
def login():
    """POST /sessions
    Validates email and password in POST request.
    Respond:
        - 401 HTTP status if email doesn't exist or the password isn't valid
        - JSON payload with a cookie attached to the response.
    """
    email = request.form.get("email")
    password = request.form.get("password")
    if email is None or password is None:
        abort(401)

    if AUTH.valid_login(email, password) is False:
        abort(401)

    session_id = AUTH.create_session(email)

    # Set cookie to the response
    response = jsonify({"email": "{}".format(email), "message": "logged in"})
    response.set_cookie("session_id", session_id)

    return response


@app.route("/sessions", methods=["DELETE"], strict_slashes=False)
def logout():
    """DELETE /session
    If the user exists, destroys the session and redirect the user
    to GET /. Otherwise, respond with a 403 HTTP status
    """
    session_id = request.cookies.get("session_id")
    if session_id is None:
        abort(403)

    user = AUTH.get_user_from_session_id(session_id)
    if user is None:
        abort(403)

    AUTH.destroy_session(user.id)
    return redirect("/", 302)


@app.route("/profile", methods=['GET'], strict_slashes=False)
def profile():
    """GET /profile
    Finds a user by session ID in request.
    If the user exists, respond with JSON payload and 200 HTTP status.
    Otherwise, respond with 403 HTTP status.
    """
    session_id = request.cookies.get("session_id")
    if session_id is None:
        abort(403)

    user = AUTH.get_user_from_session_id(session_id)
    if user is None:
        abort(403)

    return jsonify({'email': "{}".format(user.email)}), 200


@app.route("/reset_password", methods=['POST'], strict_slashes=False)
def get_reset_password_token():
    """POST /reset_password
    Resets the password of the user that correspond with the input email.

    Respond with 403 if the user is not registered. Otherwise,
    Respond with a JSON payload and a 200 HTTP satutus.
    """
    email = request.form.get('email')
    if email is None:
        abort(403)

    try:
        reset_token = AUTH.get_reset_password_token(email)
    except ValueError:
        abort(403)

    return jsonify({
        'email': '{}'.format(email),
        'reset_token': reset_token})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000", debug=True)
