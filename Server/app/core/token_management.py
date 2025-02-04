# app/core/token_management.py

from typing import Set


class TokenManager:
    """
    A class to manage token invalidation for the logout functionality.
    Uses a simple in-memory set to store invalid tokens.
    """

    _invalid_tokens: Set[str] = set()

    @classmethod
    def invalidate_token(cls, token: str) -> None:
        """
        Add a token to the invalid tokens set

        Args:
            token: The token to invalidate
        """
        cls._invalid_tokens.add(token)

    @classmethod
    def is_token_invalid(cls, token: str) -> bool:
        """
        Check if a token is in the invalid tokens set

        Args:
            token: The token to check

        Returns:
            bool: True if token is invalid, False otherwise
        """
        return token in cls._invalid_tokens

    @classmethod
    def clear_invalid_tokens(cls) -> None:
        """Clear all invalid tokens from the set"""
        cls._invalid_tokens.clear()


# Create a singleton instance
token_manager = TokenManager()