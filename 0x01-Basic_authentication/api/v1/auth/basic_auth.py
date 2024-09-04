#!/usr/bin/env python3
"""This module contain the class BasicAuth
   for basic authentication
"""
from .auth import Auth


class BasicAuth(Auth):
    """Basic Authentication class
    """
    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """Extract base64 authorization header
        """
        if authorization_header is None:
            return None

        if not isinstance(authorization_header, str):
            return None

        if authorization_header.startswith('Basic '):
            liststr = authorization_header.split()
            return liststr[1]
        else:
            return None
