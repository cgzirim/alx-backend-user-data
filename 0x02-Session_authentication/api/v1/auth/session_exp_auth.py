#!/usr/bin/env python3
""" Module to handle expiration date to a Session ID.
"""
import os
from datetime import datetime
from datetime import timedelta
from api.v1.auth.session_auth import SessionAuth


class SessionExpAuth(SessionAuth):
    """Adds an expiration date to a Session ID."""

    def __init__(self) -> None:
        """Initialize SessionExpAuth."""
        try:
            self.session_duration = int(os.getenv("SESSION_DURATION", 0))
        except ValueError:
            self.session_duration = 0

    def create_session(self, user_id: str = None) -> str:
        """Create a session ID for a user and acknowledge the time
        of creation.
        """
        session_id = super().create_session(user_id)
        if session_id is None:
            return None

        session_dictionary = {'user_id': user_id, 'created_at': datetime.now()}
        self.user_id_by_session_id[session_id] = session_dictionary

        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """Retrieves a user's ID by session_id.
        Return:
            - None if session_id is None
            -  None if user_id_by_session_id doesn’t contain any key equals
                to session_id
            - None if session_dictionary doesn’t contain a key created_at
            - user_id key from the session dictionary if self.session_duration
                is equal or under 0
            - None if the created_at + session_duration seconds are before
                the current datetime. datetime - timedelta
            - user_id from the session_dictionary
        """
        user_id = super().user_id_for_session_id(session_id)
        if user_id is None:
            return None

        session_dictionary = self.user_id_by_session_id.get(session_id)
        if session_dictionary is None:
            return None

        if self.session_duration <= 0:
            return session_dictionary.get('user_id')

        if self.user_id_by_session_id[session_id].get('created_at') is None:
            return None

        created_at = session_dictionary.get('created_at')
        if created_at is None:
            return None

        sum = created_at + timedelta(seconds=self.session_duration)
        if sum < datetime.now():
            return None

        return user_id
