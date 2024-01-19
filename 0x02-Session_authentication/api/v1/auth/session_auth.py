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
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
        Creates a Session ID for user_id
        """
        if user_id is None or not isinstance(user_id, str):
            return None

        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id

        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        A instance method that returns a UserId based on Session ID

        Args:
            session_id (str): Session ID

        Returns:
            str: User ID
        """
        if session_id is None or not isinstance(session_id, str):
            return None

        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """
        Returns a User instance based on a cookie value
        """
        if request is None:
            return None

        session_id = self.session_cookie(request)
        if session_id is None:
            return None

        user_id = self.user_id_for_session_id(session_id)
        if user_id is None:
            return None

        user = User.get(user_id)
        return user

    def destroy_session(self, request=None) -> bool:
        """
        Deletes the user session / logout
        """
        if request is None:
            return False

        session_id = self.session_cookie(request)
        if session_id is None:
            return False

        user_id = self.user_id_for_session_id(session_id)
        if user_id is None:
            return False

        del self.user_id_by_session_id[session_id]
        return True
