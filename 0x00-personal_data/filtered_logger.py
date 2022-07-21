#!/usr/bin/env python3
"""Defines the function filter_datum."""
import re
import logging
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


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    logging.basicConfig(level=logging.INFO, format=FORMAT)

    def __init__(self, fields: List[str]):
        self.fields = fields
        super(RedactingFormatter, self).__init__(self.FORMAT)

    def format(self, record: logging.LogRecord) -> str:
        """Filters values in incoming log records."""
        record.msg = filter_datum(
                list(self.fields), self.REDACTION,
                record.getMessage(), self.SEPARATOR
                )
        return super(RedactingFormatter, self).format(record)
