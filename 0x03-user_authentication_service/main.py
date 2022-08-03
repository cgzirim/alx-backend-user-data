#!/usr/bin/env python3
"""End-to-end integration test."""
import requests


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


def register_user(email: str, password: str) -> None:
    """Tests the route POST /users"""
    if not email or not password:
        return None

    data = {"email": email, "password": password}
    response = requests.post("http://localhost:5000/users", data=data)
    assert response.status_code == 200

    message = {"email": email, "message": "user created"}
    assert response.json() == message


def log_in_wrong_password(email: str, password: str) -> None:
    """Test the route POST /sessions with the wrong password."""
    if not email or not password:
        return None

    data = {"email": email, "password": password}
    response = requests.post("http://localhost:5000/sessions", data=data)
    assert response.status_code == 401


def log_in(email: str, password: str) -> str:
    """Test the POST /sessions route with the right password.

    Returns session ID in the cookie of the response
    """
    if not email or not password:
        return None

    data = {"email": email, "password": password}
    response = requests.post("http://localhost:5000/sessions", data=data)
    print(response.status_code)
    assert response.status_code == 200

    message = {"email": email, "message": "logged in"}
    assert response.json() == message

    session_id = response.cookies.get("session_id")
    assert session_id is not None

    return session_id


def profile_unlogged() -> None:
    """Test GET /profile route without including a session_id to the GET
    request.
    """
    response = requests.get("http://localhost:5000/profile")
    assert response.status_code == 403


def profile_logged(session_id: str) -> None:
    """Test GET /profile route with a session_id included in the Get
    request.
    """
    if session_id is None:
        return None

    cookie = {"session_id": session_id}
    response = requests.get("http://localhost:5000/profile", cookies=cookie)

    assert response.status_code == 200

    assert response.json() == {"email": EMAIL}


def log_out(session_id: str) -> None:
    """Test DELETE /session route"""
    if session_id is None:
        return None

    cookie = {"session_id": session_id}
    response = requests.delete(
        "http://localhost:5000/sessions", cookies=cookie)

    assert response.status_code == 200
    assert response.json() == {"message": "Bienvenue"}


def reset_password_token(email: str) -> str:
    """Test POST /reset_password."""
    if email is None:
        return None

    data = {"email": email}
    response = requests.post("http://localhost:5000/reset_password", data=data)

    assert response.status_code == 200

    reset_token = response.json().get("reset_token")
    message = {"email": EMAIL, "reset_token": reset_token}

    assert response.json() == message


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """Test PUT /reset_password"""
    if not email or not reset_token or not new_password:
        return None

    data = {
        "email": email,
        "reset_token": reset_token,
        "password": new_password
    }

    response = requests.put("http://localhost:5000/reset_password", data=data)
    assert response.status_code == 200

    message = {"email": "{}".format(email), "message": "Password updated"}
    assert response.json() == message


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
