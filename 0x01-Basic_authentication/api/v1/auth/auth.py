#!/usr/bin/env python3

"""
A module to manage API authentication
"""

from flask import request


class Auth():
    """
    A class to manage Api authentication
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Placeholder method for authentication check.

        Args:
        - path (str): The path of the request.
        - excluded_paths (List[str]): List of paths to be excluded
        from authentication check.

        Returns:
        - bool: Always returns False for now.
        """
        return False

    def authorization_header(self, request=None) -> str:
        """
        Placeholder method for retrieving the Authorization header.

        Args:
        - request: Flask request object.

        Returns:
        - str: Always returns None for now.
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Placeholder method for retrieving the current user.

        Args:
        - request: Flask request object.

        Returns:
        - TypeVar('User'): Always returns None for now.
        """
        return None
