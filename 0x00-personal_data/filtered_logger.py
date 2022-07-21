#!/usr/bin/env python3
"""Defines the function filter_datum."""
import re
import logging
from os import getenv
import mysql.connector
from typing import List


PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def get_db() -> mysql.connector.connection.MySQLConnection:
    """Returns a connector to MySQL database."""
    my_db = mysql.connector.connect(
        host=getenv("PERSONAL_DATA_DB_HOST"),
        user=getenv("PERSONAL_DATA_DB_USERNAME"),
        password=getenv("PERSONAL_DATA_DB_PASSWORD"),
        database=getenv("PERSONAL_DATA_DB_NAME"),
        auth_plugin='mysql_native_password'
    )
    return my_db


def main() -> None:
    """Display all rows in the user table of a database."""
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users;")
    message = cursor
    logger = get_logger()
    logger.info(message)

    cursor.close()
    db.close()


def filter_datum(
    fields: List[str], redaction: str, message: str, separator: str
) -> str:
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
            "{}=.*?{}".format(f, separator),
            "{}={}{}".format(f, redaction, separator),
            message,
        )
    return message


def get_logger() -> logging.Logger:
    """Creates and returns a logger."""
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(RedactionFormatter(list(PII_FIELDS)))
    logger.addHandler(stream_handler)

    return logger


class RedactingFormatter(logging.Formatter):
    """Redacting Formatter class"""

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
            list(
                self.fields), self.REDACTION,
            record.getMessage(), self.SEPARATOR
        )
        return super(RedactingFormatter, self).format(record)


if __name__ == "__main__":
    main()
