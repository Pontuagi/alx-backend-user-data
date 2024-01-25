#!/usr/bin/env python3

"""DB module
"""
import logging
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import NoResultFound, InvalidRequestError
from user import Base, User


logging.getLogger('sqlalchemy').setLevel(logging.WARNING)


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=True)
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

    def add_user(self, email: str, hashed_password: str) -> User:
        """
        Add a new user to the database
        """
        new_user = User(email=email, hashed_password=hashed_password)
        self._session.add(new_user)
        self._session.commit()
        return new_user

    def find_user_by(self, **kwargs) -> User:
        """
        Find a user in the database based on the provided filter arguments.
        """
        try:
            user = self._session.query(User).filter_by(**kwargs).first()
            if user is None:
                raise NoResultFound("No such user found")
            return user
        except NoResultFound:
            raise
        except InvalidRequestError as e:
            raise InvalidRequestError("Invalid query arguments: {}".format(e))

    def update_user(self, user_id: int, **kwargs) -> None:
        """
        Update a user in the database based on the provided user_id and
        keyword arguments.
        """
        try:
            # Find the user by user_id
            user = self.find_user_by(id=user_id)

            # Update user attributes based on keyword arguments
            for key, value in kwargs.items():
                if hasattr(User, key):
                    setattr(user, key, value)
                else:
                    raise ValueError(f"Invalid attribute: {key}")

            # Commit changes to the database
            self._session.commit()

        except NoResultFound:
            raise NoResultFound(f"No user found with user_id: {user_id}")

        except InvalidRequestError as e:
            raise InvalidRequestError(f"Invalid query: {e}")
