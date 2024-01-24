#!/usr/bin/env python3

"""
Auth module
"""

import bcrypt


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
