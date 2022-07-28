#!/usr/bin/env python3
""" User Session module
"""
from models.base import Base


class UserSession(Base):
    """Session in database"""

    def __init__(self, *args: list, **kwargs: dict):
        """Initialize session instance."""
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get("user_id")
        self.session_id = kwargs.get("session_id")
