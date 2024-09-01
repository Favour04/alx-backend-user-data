#!/usr/bin/env python3
import re
"""
    logging module
"""


def filter_datum(fields, redaction, message, separator):
    """returns the log message obfuscated."""
    for field in fields:
        pattern = f'{field}=[^{separator}]*'
        message = re.sub(pattern, f'{field}={redaction}', message)
    return message
