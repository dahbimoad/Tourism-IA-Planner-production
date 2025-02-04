# app/core/token_management.py

from typing import Set, Dict
from datetime import datetime, timedelta
import logging
import threading

logger = logging.getLogger(__name__)


class TokenManager:
    """
    A class to manage token invalidation for the logout functionality.
    Uses thread-safe collections to store invalid tokens.
    """

    def __init__(self):
        self._invalid_tokens: Set[str] = set()
        self._user_tokens: Dict[int, Set[str]] = {}
        self._lock = threading.Lock()

    def invalidate_token(self, token: str, user_id: int = None) -> None:
        """
        Add a token to the invalid tokens set

        Args:
            token: The token to invalidate
            user_id: Optional user ID to track token ownership
        """
        with self._lock:
            self._invalid_tokens.add(token)
            if user_id:
                if user_id not in self._user_tokens:
                    self._user_tokens[user_id] = set()
                self._user_tokens[user_id].add(token)
            logger.info(f"Token invalidated for user {user_id}")

    def invalidate_all_user_tokens(self, user_id: int) -> None:
        """
        Invalidate all tokens for a specific user

        Args:
            user_id: The user ID whose tokens should be invalidated
        """
        with self._lock:
            if user_id in self._user_tokens:
                for token in self._user_tokens[user_id]:
                    self._invalid_tokens.add(token)
                logger.info(f"All tokens invalidated for user {user_id}")

    def is_token_invalid(self, token: str) -> bool:
        """
        Check if a token is in the invalid tokens set

        Args:
            token: The token to check

        Returns:
            bool: True if token is invalid, False otherwise
        """
        with self._lock:
            return token in self._invalid_tokens

    def clear_invalid_tokens(self) -> None:
        """Clear expired tokens from the invalid tokens set"""
        with self._lock:
            self._invalid_tokens.clear()
            self._user_tokens.clear()
            logger.info("Invalid tokens cleared")

    def get_user_tokens(self, user_id: int) -> Set[str]:
        """
        Get all tokens associated with a user

        Args:
            user_id: The user ID to check

        Returns:
            Set[str]: Set of tokens belonging to the user
        """
        with self._lock:
            return self._user_tokens.get(user_id, set()).copy()

    def remove_user_token(self, user_id: int, token: str) -> None:
        """
        Remove a specific token from a user's token set

        Args:
            user_id: The user ID
            token: The token to remove
        """
        with self._lock:
            if user_id in self._user_tokens:
                self._user_tokens[user_id].discard(token)
                self._invalid_tokens.discard(token)
                logger.info(f"Token removed for user {user_id}")


# Create a singleton instance
token_manager = TokenManager()