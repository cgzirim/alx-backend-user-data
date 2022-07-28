#!/usr/bin/env python3
"""Defines the class SessionAuth"""
import uuid
from models.user import User
from api.v1.auth.auth import Auth


class SessionAuth(Auth):
    """Handles session authentication."""

    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """Generates a Session ID.
        Parameter:
            - user_id: User ID
        Return:
            - None if user_id is None
            - None if user_id is not a string
        """
        if user_id is None or isinstance(user_id, str) is False:
            return None

        session_id = str(uuid.uuid4())

        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """Returns a user ID in the user_id_by_session_Id attr.
        Parameters:
            - session_Id: A session ID
        Returns:
            - None if session_id is None
            - Return None if session_id is not a string
        """
        if session_id is None or isinstance(session_id, str) is False:
            return None

        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None) -> str:
        """Retrieves a User instance based on a cookie value.
        Parameter:
            - request: A HTTP request
        Returns:
            - None if request is None
            - User instance
        """
        cookie_id = self.session_cookie(request)
        if cookie_id is None:
            return None

        user_id = self.user_id_for_session_id(cookie_id)
        if user_id is None:
            return None

        return User.get(user_id)

    def destroy_session(self, request=None):
        """Deletes a user session/logout.
        Parameter:
            - request: A HTTP request
        Returns:
            - False if the request is equal to None
            - False if the request doesn’t contain the Session ID cookie
        """
        session_id = self.session_cookie(request)
        if session_id is None:
            return False

        if self.user_id_for_session_id(session_id) is None:
            return False

        del self.user_id_by_session_id[session_id]
        return True
