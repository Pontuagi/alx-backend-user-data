#!/usr/bin/env python3

"""
Auth module
"""

import bcrypt
import uuid
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound, InvalidRequestError


def _hash_password(password: str) -> bytes:
    """
    Hash and salt the given password using bcrypt.

    Args:
        password (str): The input password string.

    Returns:
        bytes: The salted hash of the input password.
    """
    salt = bcrypt.gensalt()

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)

    return hashed_password


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        Register a new user.

        Args:
            email (str): Email of the user.
            password (str): Password of the user.

        Returns:
            User: The User object representing the registered user.

        Raises:
            ValueError: If a user with the provided email already exists.
        """
        # Check if the user already exists
        try:
            self._db.find_user_by(email=email)
        except NoResultFound:
            # User does not exist, proceed with registration
            hashed_password = _hash_password(password)
            new_user = self._db.add_user(email, hashed_password)
            return new_user
        else:
            raise ValueError(f"User {email} already exists.")

    def valid_login(self, email: str, password: str) -> bool:
        """Check if login credentials are valid."""
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return False
        except InvalidRequestError:
            return False
        return bcrypt.checkpw(password.encode('utf-8'), user.hashed_password)

    def _generate_uuid() -> str:
        """Generate a string representation of a new UUID."""
        return str(uuid.uuid4())
