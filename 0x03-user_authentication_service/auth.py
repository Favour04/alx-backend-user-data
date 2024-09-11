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

    def get_user_from_session_id(self, session_id: str) -> User:
        if session_id is None:
            return None

        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """Destroy session
        """
        if user_id is None:
            return None

        self._db.update_user(user_id, session_id=None)
        return None

    def get_reset_password_token(self, email: str) -> str:
        """This generate tokn to reset password
        """
        try:
            user = self._db.find_user_by(email=email)
            tkn = _generate_uuid()
            self._db.update_user(user.id, reset_token=tkn)
            return tkn
        except NoResultFound:
            raise ValueError

    def update_password(self, reset_token: str, password: str) -> str:
        """Updates pswd
        """
        try:
            user = self._db.find_user_by(reset_token=reset_token)
            if password:
                new_hpswd = _hash_password(password)
            else:
                raise ValueError
            self._db.update_user(user.id, {"hash_password": new_hpswd,
                                           "reset_token": None})
        except NoResultFound:
            raise ValueError
