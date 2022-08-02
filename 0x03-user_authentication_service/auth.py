#!/usr/bin/env python3
"""Auth module"""
import uuid
import bcrypt
from db import DB
from db import DB
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """Hash password with bcrypt.hashpw"""
    if type(password) != str:
        return None

    salt = bcrypt.gensalt()
    hashed_pwd = bcrypt.hashpw(bytes(password, "utf-8"), salt)

    return hashed_pwd

def _generate_uuid():
        """Returns a string representation of a new UUID."""
        return str(uuid.uuid4())


class Auth:
    """Auth class to interact with the authentication database."""

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> bytes:
        """Registers a user"""
        if not email or not password:
            return None

        if not isinstance(email, str) or not isinstance(password, str):
            return None

        try:
            self._db.find_user_by(email=email)
            raise ValueError("User {} already exists".format(email))
        except NoResultFound:
            hashed_pwd = _hash_password(password)
            return self._db.add_user(email, hashed_pwd)

    def valid_login(self, email: str, password: str) -> bool:
        """Validates a user's credentials.
        Return:
            - False if email doesn't exist
            - False if password doesn't match password for given email
            - True is email and password are correct.
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return False

        user_password = user.hashed_password
        encoded_password = password.encode()

        if bcrypt.checkpw(encoded_password, user_password):
            return True

        return False

    def create_session(self, email: str) -> str:
        """Create session for the user and returns the session ID."""
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return None

        setattr(user, "session_id", _generate_uuid())
        return self.session_id
