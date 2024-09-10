#!/usr/bin/env python3
"""Authentication module
"""
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """Hashes paswords
    """
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt)


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """This method is used to create new user
        """
        try:
            if self._db.find_user_by(email=email):
                raise ValueError(f'User {email} already exists.')
        except NoResultFound:
            if not isinstance(password, bytes):
                password = _hash_password(password)

            user = self._db.add_user(email, password)
            return user
