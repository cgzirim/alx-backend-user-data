#!/usr/bin/env python3
"""Auth module"""
import uuid
import bcrypt
from db import DB
from typing import Union
from user import User
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """Hash password with bcrypt.hashpw"""
    if type(password) != str:
        return None

    salt = bcrypt.gensalt()
    hashed_pwd = bcrypt.hashpw(bytes(password, "utf-8"), salt)

    return hashed_pwd


def _generate_uuid() -> str:
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

        user.session_id = _generate_uuid()

        return user.session_id

    def get_user_from_session_id(self, session_id: str) -> Union[None, User]:
        """Finds a user by session ID.
        Returns user instance if found; otherwise, returns None.
        """
        if session_id is None or isinstance(session_id, str) is False:
            return None

        try:
            user = self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None

        return user

    def destroy_session(self, user_id: int) -> None:
        """Updates corresponding user's session ID to None."""
        if user_id is None:
            return None
        try:
            user = self._db.find_user_by(id=user_id)
            user.session_id = None
        except NoResultFound:
            return None
        return None

    def get_reset_password_token(self, email: str) -> str:
        """Generate a UUID and update the user's reset_token database field.

        Returns the generated UUID if the user corresponding to the email
        exists. Otherwise, raise a ValueError.
        """
        if email is None or isinstance(email, str) is False:
            raise ValueError

        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            raise ValueError

        user.reset_token = _generate_uuid()

        return user.reset_token

    def update_password(self, reset_token: str, password: str) -> None:
        """Updates a user password."""
        if not reset_token or not password:
            return None

        try:
            user = self._db.find_user_by(reset_token=reset_token)
        except NoResultFound:
            raise None

        user.hashed_password = _hash_password(password)
        return None
