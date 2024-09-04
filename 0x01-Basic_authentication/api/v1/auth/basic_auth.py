#!/usr/bin/env python3
"""This module contain the class BasicAuth
   for basic authentication
"""
from .auth import Auth
import base64
from typing import TypeVar
from models.user import User


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

    def decode_base64_authorization_header(self, base64_authorization_header:
                                           str) -> str:
        """Decode base64 authorization header
        """
        if base64_authorization_header is None:
            return None

        if not isinstance(base64_authorization_header, str):
            return None

        try:
            return base64.b64decode(base64_authorization_header).decode(
                                    'utf-8')
        except Exception:
            return None

    def extract_user_credentials(self, decoded_base64_authorization_header:
                                 str) -> (str, str):
        """Extract user credentials
        """
        if decoded_base64_authorization_header is None:
            return None, None

        if not isinstance(decoded_base64_authorization_header, str):
            return None, None

        if ':' not in list(decoded_base64_authorization_header):
            return None, None
        else:
            credentails = decoded_base64_authorization_header.split(':')
            return credentails[0], credentails[1]

    def user_object_from_credentials(self, user_email:
                                     str, user_pwd: str) -> TypeVar('User'):
        """Create user object from credentials
        """
        if not isinstance(user_email, str):
            return None
        
        if not isinstance(user_pwd, str):
            return None

        User.load_from_file()
        if User.count() == 0:
            return None
        elif User.search({'email': user_email}) is not None:
            for user in User.search({'email': user_email}):
                if user.is_valid_password(user_pwd):
                    return user
                else:
                    return None
        else:
            return None
            
