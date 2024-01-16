#!/usr/bin/env python3

"""
BasicAuth Module
"""
from api.v1.auth.auth import Auth
from models.user import User
import base64
from typing import TypeVar


class BasicAuth(Auth):
    """
    A class that inherits from class Auth
    """
    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """
        Extract the Base64 part of the Authorization header for Basic
        Authentication.

        Args:
        - authorization_header (str): The Authorization header.

        Returns:
        - str: The Base64 part of the Authorization header,
        or None if not valid.
        """
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith('Basic '):
            return None

        base64_auth = authorization_header.split(' ', 1)[1]
        return base64_auth

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """
         Decode the Base64 Authorization header.

        Args:
        - base64_authorization_header (str): The Base64 Authorization header.

        Returns:
        - str: The decoded value as UTF-8 string, or None if not valid.
        """
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None

        try:
            # Attempt to decode the Base64 string
            decoded_value = base64.b64decode(
                    base64_authorization_header).decode('utf-8')
            return decoded_value
        except Exception as e:
            return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> (str, str):
        """
        Extract the user email and password from the Base64 decoded value.

        Args:
        - decoded_base64_authorization_header (str): The decoded
        Base64 Authorization header.

        Returns:
        - tuple: (str, str) representing user email and password,
        or (None, None) if not valid.
        """
        if decoded_base64_authorization_header is None:
            return None, None
        if not isinstance(decoded_base64_authorization_header, str):
            return None, None
        if ':' not in decoded_base64_authorization_header:
            return None, None

        user_email, user_password = decoded_base64_authorization_header.split(
                ':', 1)
        return user_email, user_password

    def user_object_from_credentials(
            self,
            user_email: str,
            user_pwd: str) -> TypeVar('User'):
        """
        Get the User instance based on email and password.

        Args:
        - user_email (str): User's email.
        - user_pwd (str): User's password.

        Returns:
        - TypeVar('User'): User instance or None if not found or
        password doesn't match.
        """
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None
        users = User.search({'email': user_email})

        if not users:
            return None

        # Check if user_pwd is the password of the User instance found
        for user in users:
            if user.is_valid_password(user_pwd):
                return user

        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Retrieve the User instance for a request.

        Args:
        - request: Flask request object.

        Returns:
        - TypeVar('User'): User instance or None if not found or
        credentials are invalid.
        """
        auth_header = request.headers.get('Authorization')
        base64_auth_header = self.extract_base64_authorization_header(
                auth_header)
        decoded_auth_header = self.decode_base64_authorization_header(
                base64_auth_header)
        user_email, user_pwd = self.extract_user_credentials(
                decoded_auth_header)
        user_instance = self.user_object_from_credentials(
                user_email, user_pwd)

        return user_instance
