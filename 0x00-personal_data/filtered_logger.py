#!/usr/bin/env python3
import re
def filter_datum(fields, redaction, message, separator):
    for field in fields:
        message = re.sub(f'{field}=[^{separator}]*', f'{field}={redaction}', message)
    return message
