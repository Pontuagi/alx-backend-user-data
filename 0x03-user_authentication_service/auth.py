#!/usr/bin/env python3

"""
Auth module
"""

import bcrypt
import uuid
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError


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


def _generate_uuid() -> str:
    """Generate a string representation of a new UUID."""
    return str(uuid.uuid4())


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

    def create_session(self, email: str) -> str:
        """
        Create a session fo the user identified by the email
        """
        try:
            user = self._db.find_user_by(email=email)
            session_id = str(uuid.uuid4())
            self._db.update_user(user.id, session_id=session_id)
            return session_id
        except NoResultFound:
            raise ValueError

    def get_user_from_session_id(self, session_id: str) -> User:
        """Get the user corresponding to a session ID.

        Args:
            session_id (str): The session ID to look up.

        Returns:
            User or None: The corresponding User object if found,
            otherwise None.
        """
        if session_id is None:
            return None

        try:
            user = self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            user = None

        return user

    def destroy_session(self, user_id: int) -> None:
        """Destroy the session for the given user.

        Args:
            user_id (int): The ID of the user.

        Returns:
            None
        """
        self._db.update_user(user_id, session_id=None)

    def get_reset_password_token(self, email: str) -> str:
        """
        Get a reset password token for the user with the given email.

        Args:
            email (str): The email of the user.

        Returns:
            str: The reset password token.

        Raises:
            ValueError: If the user with the provided email does not exist.
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            raise ValueError

        # Generate a new UUID as the reset token
        reset_token = str(uuid.uuid4())

        # Update the user's reset_token field in the database
        self._db.update_user(user.id, reset_token=reset_token)

        return reset_token

    def update_password(self, reset_token: str, password: str) -> None:
        """
        Update user's password using reset_token.
        """
        try:
            user = self._db.find_user_by(reset_token=reset_token)
            if user is None:
                raise ValueError

            # Hash the new password
            hashed_password = self._hash_password(password)

            # Update user's hashed_password and reset_token fields
            user.hashed_password = hashed_password
            user.reset_token = None

            # Commit changes to the database
            self._db._session.commit()

        except Exception as e:
            raise ValueError
