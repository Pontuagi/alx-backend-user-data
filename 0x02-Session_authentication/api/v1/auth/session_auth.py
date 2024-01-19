#!/usr/bin/env python3

"""
SessionAuth Module
"""
import uuid
from api.v1.auth.auth import Auth


class SessionAuth(Auth):
    """
    Session authentication class
    A class that inherits from Auth

    Args:
        user_id (str):;  User ID

    Returns:
        str: Session ID
    """
    user_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
        Creates a Session ID for user_id
        """
        if user_id is None or not isintance(user_id, str):
            return None

        session_id = str(uuid.uuid4())
        self.user_session_id[session_id] = user_id

        return session_id
