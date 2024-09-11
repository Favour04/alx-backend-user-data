#!/usr/bin/env python3
"""Authentication module
"""
import bcrypt
from db import DB
from user import User
from uuid import uuid4
from sqlalchemy.orm.exc import NoResultFound


def _generate_uuid() -> str:
    """Returns new uuid
    """
    return str(uuid4())


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

    def valid_login(self, email: str, password: str) -> bool:
        """Validate Login
        """
        try:
            user = self._db.find_user_by(email=email)
            return bcrypt.checkpw(password.encode("utf-8"),
                                  user.hashed_password)
        except NoResultFound:
            return False

    def create_session(self, email: str) -> str:
        """Create a section id for a user
        """
        try:
            user = self._db.find_user_by(email=email)
            user.session_id = _generate_uuid()
            return user.session_id
        except NoResultFound:
            return None
