#!/usr/bin/env python3

"""
BasicAuth Module
"""
from api.v1.auth.auth import Auth
import base64


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
