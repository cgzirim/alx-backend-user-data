#!/usr/bin/env python3
"""Auth module"""
import bcrypt
from db import DB
from sqlalchemy.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """Hash password with bcrypt.hashpw"""
    salt = bcrypt.gensalt()

    hashed_pwd = bcrypt.hashpw(bytes(password, "utf-8"), salt)

    return hashed_pwd


class Auth:
    """Auth class to interact with the authentication database."""

    def __init__(self):
        self._db = DB()

    def register_user(self, email, password):
        """Registers a user"""
        try:
            self._db.find_user_by(email=email)
            raise ValueError("User {} already".format(email))
        except NoResultFound:
            hashed_pwd = _hash_password(password)
            return self._db.add_user(email, hashed_pwd)
