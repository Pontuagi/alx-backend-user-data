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
