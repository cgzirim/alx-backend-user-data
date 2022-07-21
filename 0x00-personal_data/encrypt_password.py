#!/usr/bin/env python3
"""Encrypting passwords."""
import bcrypt


def hash_password(password: str) -> bytes:
    """Hashes a password."""
    password = bytes(password, "utf-8")
    hashed = bcrypt.hashpw(password, bcrypt.gensalt())
    return hashed


def is_valid(hashed_password: bytes, password: str) -> bool:
    """Validate hat the provided password matches the hashed password."""
    password = bytes(password, "utf-8")
    if bcrypt.checkpw(password, hashed_password):
        return True
    return False
