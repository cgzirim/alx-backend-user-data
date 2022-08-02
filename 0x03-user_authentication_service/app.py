#!/usr/bin/env python3
"""Basic Flask app."""
from auth import Auth
from flask import Flask, jsonify
from flask import request, abort


AUTH = Auth()
app = Flask(__name__)


@app.route('/', methods=['GET'], strict_slashes=False)
def hello() -> str:
    """Returns JSON payload."""
    return jsonify({'message': 'Bienvenue'})


@app.route('/users', methods=['POST'], strict_slashes=False)
def users():
    """Registers a user and returns a JSON payload."""
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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000", debug=True)
