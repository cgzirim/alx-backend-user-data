#!/usr/bin/env python3
"""Defines Auth class."""
from flask import request
from typing import List
from typing import TypeVar


class Auth:
    """Manages the API authentication."""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Defines which routes don't need authentication."""
        if path is None:
            return True

        if path[-1] != "/":
            path += "/"

        for p in excluded_paths:
            if p[-2] == "*":
                if path[8:12] == p[8:12]:
                    return False

        if excluded_paths is False or path not in excluded_paths:
            return True

        return False

    def authorization_header(self, request=None) -> str:
        """Returns Authorization data if Authorization exists in requests."""
        if request is None:
            return None
        if request.headers.get("Authorization") is None:
            return None

        return request.headers.get("Authorization")

    def current_user(self, request=None) -> TypeVar("User"):
        """stuff"""
        return None
