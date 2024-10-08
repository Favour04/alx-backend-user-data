#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from user import Base, User
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError


class DB:
    """DB class
    """
    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def new(self, obj) -> None:
        """Add obj to the current session
        """
        self._session.add(obj)

    def save(self) -> None:
        """Save obj to the database
        """
        self._session.commit()

    def add_user(self, email: str, hashed_password: str) -> User:
        """Add a user to the database
        """
        try:
            user = User(email=email, hashed_password=hashed_password)
            self.new(user)
            self.save()
            return user
        except Exception as e:
            self._session.rollback()
            raise e

    def find_user_by(self, **kwargs) -> User:
        """Find a user by a given attribute
        """
        if not kwargs:
            raise InvalidRequestError
        try:
            user = self._session.query(User).filter_by(**kwargs).one()
            return user
        except NoResultFound as e:
            raise e

    def update_user(self, user_id: int, **kwargs) -> None:
        """Update a particular user
        """
        user = self.find_user_by(id=user_id)
        for key, value in kwargs.items():
            if hasattr(user, key):
                setattr(user, key, value)
            else:
                raise ValueError

        self.save()
