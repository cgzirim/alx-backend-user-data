#!/usr/bin/env python3
"""Defines the function filter_datum."""
import re
from typing import List


def filter_datum(
        fields: List[str], redaction: str,
        message: str, separator: str) -> str:
    """Returns an obfuscated log message.

    Parameters:
        fields: a list of strings representing all fields to obfuscate
        redaction: a string representing by what the field will be obfuscated
        message: a string representing the log line
        separator: a string representing by which character is separating all
                fields in the message.
    """
    for f in fields:
        message = re.sub(
                '{}=.*?{}'.format(f, separator),
                '{}={}{}'.format(f, redaction, separator),
                message
                )
    return message
