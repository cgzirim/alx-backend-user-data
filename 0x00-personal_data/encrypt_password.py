#!/usr/bin/env python3
"""Encrypting passwords."""
import bcrypt


def hash_password(password: str) -> bytes:
    """Hashes a password."""
    password = bytes(password, "utf-8")
    hashed = bcrypt.hashpw(password, bcrypt.gensalt())
    return hashed
