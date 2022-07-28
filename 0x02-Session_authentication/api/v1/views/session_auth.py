#!/usr/bin/env python3
""" Module of Session authentication routes.
"""
import os
import hashlib
from api.v1.views import app_views
from flask import abort, jsonify, request
from models.user import User


@app_views.route("/auth_session/login", methods=["POST"], strict_slashes=False)
def login():
    """POST api/v1/auth_session/login

    Validates email and password in POST request.
    Returns:
        - Error 400 if the email is missing
        - Error 400 if password is missing
        - Error 404 if no user is found for the email
        - Error 401 if the password is wrong
        - User's json representation with a cookie attached to the response.
    """
    user_email = request.form.get("email")
    if user_email is None:
        return jsonify({"error": "email missing"}), 400

    user_pwd = request.form.get("password")
    if user_pwd is None:
        return jsonify({"error": "password missing"}), 400

    user = User.search({"email": user_email})
    if len(user) == 0:
        return jsonify({"error": "no user found for this email"}), 404

    user = user[0]
    if user.is_valid_password(user_pwd) is False:
        return jsonify({"error": "wrong password"}), 401

    user_pwd = hashlib.sha256(user_pwd.encode()).hexdigest().lower()
    if user_pwd != user.password:
        return jsonify({"error": "wrong password"}), 401

    # Create a Session ID for the user
    from api.v1.app import auth

    session_id = auth.create_session(user.id)

    # Set cookie to the response
    resp = jsonify(user.to_json())
    session_key = os.getenv("SESSION_NAME")
    resp.set_cookie(session_key, session_id)

    return resp


@app_views.route("/auth_session/logout", methods=["DELETE"],
                 strict_slashes=False)
def logout():
    """Deletes the a user's session."""
    from api.v1.app import auth

    if auth.destroy_session(request) is False:
        abort(404)

    return jsonify({}), 200
