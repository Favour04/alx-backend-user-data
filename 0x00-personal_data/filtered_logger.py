#!/usr/bin/env python3
import re
from typing import List
"""This module contains a function that returns the log message obfuscated
"""


def filter_datum(fields: List[str], redaction: str, message: str, separator: str) -> str:
    for field in fields:
        pattern = f'{field}=[^{separator}]*'
        message = re.sub(pattern, f'{field}={redaction}', message)
    return message
