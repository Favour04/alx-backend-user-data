#!/usr/bin/python3
# import logging
import re

# logger = logging.getLogger('__name__')
# logger.setLevel(logging.INFO)

# stream_handler = logging.StreamHandler()
# formater = logging.Formatter('%(message)s')

# stream_handler.setFormatter(formater)

# logger.addHandler(stream_handler)

def filter_datum(fields: list, redaction: str, message: str, separator: str) -> str:
    for field in fields:
        pattern = f'{field}=[^{separator}]*'
        message = re.sub(pattern, f'{field}={redaction}', message)
    return message
