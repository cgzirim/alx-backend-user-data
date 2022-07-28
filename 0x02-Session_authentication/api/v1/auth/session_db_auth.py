#!/usr/bin/env python3
"""Defines the class SessionDBAuth"""
import uuid
from datetime import datetime
from datetime import timedelta
from models.user import User
from models.user_session import UserSession
from api.v1.auth.session_exp_auth import SessionExpAuth


class SessionDBAuth(SessionExpAuth):
    """Handles storage of user session in a db."""

    def create_session(self, user_id: str = None) -> str:
        """Creates and stores a new intance of UserSession."""
        session_id = super().create_session(user_id)
        if session_id is None:
            return None

        kwargs = {'user_id': user_id, 'session_id': session_id}
        user_session = UserSession(**kwargs)
        user_session.save()
        UserSession.save_to_file()

        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        if session_id is None or type(session_id) != str:
            return None

        UserSession.load_from_file()
        session = UserSession.search({'session_id': session_id})
        if len(session) == 0:
            return None

        expired_time = session.created_at + \
            timedelta(seconds=self.session_duration)

        if expired_time < datetime.utcnow():
            return None

        return session[0]['user_id']

    def destroy_session(self, request=None):
        """Destroys the UserSession"""
        session_id = self.session_cookie(request)
        if session_id is None:
            return False

        if self.user_id_for_session_id(session_id) is None:
            return False

        del self.user_id_by_session_id[session_id]
        return True
