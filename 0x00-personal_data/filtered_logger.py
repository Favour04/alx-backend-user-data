#!/usr/bin/env python3
import re
"""This module contains a function that returns the log message obfuscated
"""


def filter_datum(fields, redaction, message, separator):
    for field in fields:
        pattern = f'{field}=[^{separator}]*'
        message = re.sub(pattern, f'{field}={redaction}', message)
    return message
