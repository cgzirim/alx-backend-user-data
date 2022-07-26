#!/usr/bin/env python3
"""Defines BasicAuth class."""
import base64
import hashlib
from genericpath import isfile
from os import path
from models.user import User
from typing import Tuple, TypeVar
from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """Authenticate using Basic method."""

    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """Extracts base64 encoding from an authorization header."""
        if authorization_header is None\
                or type(authorization_header) != str\
                or authorization_header[0:6] != "Basic ":
            return None

        return authorization_header[6:]

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """Decodes a base64 encoding."""
        if base64_authorization_header is None\
                or type(base64_authorization_header) != str:
            return None

        try:
            ba_header = base64_authorization_header
            base64.b64encode(base64.b64decode(ba_header)) == ba_header
        except Exception:
            return None

        return base64.b64decode(base64_authorization_header).decode('utf-8')

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> Tuple[str, str]:
        """Extracts user credidentials from base64 encoding."""
        dba_header = decoded_base64_authorization_header
        if dba_header is None\
                or type(dba_header) != str\
                or ":" not in dba_header:
            return (None, None)

        return (dba_header[:dba_header.index(":")],
                dba_header[dba_header.index(":") + 1:])

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """Returns User instance base on his email and password."""
        if user_email is None or type(user_email) != str\
                or user_pwd is None or type(user_pwd) != str:
            return None
        file_path = ".db_User.json"
        if path.isfile(file_path) is False:
            return None

        if User.all():
            users =  User.search({"email": user_email})
            if len(users) == 0:
                return None
            user_pwd = hashlib.sha256(user_pwd.encode()).hexdigest().lower()
            if users[0].password != user_pwd:
                return None
            return users[0]
        return None
        
    def current_user(self, request=None) -> TypeVar('User'):
        """Retrieves the User instance for a request."""
        auth_header = self.authorization_header(request)
        if auth_header is None:
            return None

        b64_endcoding = self.extract_base64_authorization_header(auth_header)
        if b64_endcoding is None:
            return None
        
        b64_decoded = self.decode_base64_authorization_header(b64_endcoding)
        if b64_decoded is None:
            return None

        user_cred = self.extract_user_credentials(b64_decoded)
        if user_cred is None:
            return None

        user_obj = self.user_object_from_credentials(user_cred[0], user_cred[1])
        if user_obj is None:
            return None

        return user_obj
        