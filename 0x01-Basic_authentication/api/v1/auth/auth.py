#!/usr/bin/env python3
"""Module for the authentication views
"""
from flask import request
from typing import List, TypeVar


class Auth:
    """Auth class
    """
    def tog_str(self, string: str) -> str:
        """This method add / or remove slash
           from a string for / resilient comparison
        """
        if string[-1] != '/':
            string = f'{string}/'
        else:
            string = string[:-1]

        return string

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Require authentication
        """
        if path is None:
            return True

        if excluded_paths is None or not excluded_paths:
            return True

        if path in excluded_paths or self.tog_str(path) in excluded_paths:
            return False
        else:
            return True

    def authorization_header(self, request=None) -> str:
        """Authorization header
        """
        return None

    def current_user(self, request=None) -> TypeVar('user'):
        """Current user
        """
        return None
