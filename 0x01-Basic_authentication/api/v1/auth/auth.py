#!/usr/bin/env python3

"""
A module to manage API authentication
"""

from typing import List, TypeVar
from flask import request


class Auth():
    """
    A class to manage Api authentication
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Check if authentication is required for the given path.

        Args:
        - path (str): The path of the request.
        - excluded_paths (List[str]): List of paths to be excluded
          from authentication check.

        Returns:
        - bool: True if authentication is required, False otherwise.
        """
        if path is None:
            return True
        if excluded_paths is None or not excluded_paths:
            return True

        path = path.rstrip('/')
        excluded_paths = [p.rstrip('/') for p in excluded_paths]

        return path not in excluded_paths

    def authorization_header(self, request=None) -> str:
        """
        Retrieve the value of the Authorization header from the Flask request.

        Args:
        - request: Flask request object.

        Returns:
        - str: The value of the Authorization header or None if not present.
        """
        if request is None:
            return None
        if 'Authorization' not in request.headers:
            return None

        return request.headers['Authorization']

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Placeholder method for retrieving the current user.

        Args:
        - request: Flask request object.

        Returns:
        - TypeVar('User'): Always returns None for now.
        """
        return None
