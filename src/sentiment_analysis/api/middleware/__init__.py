"""
Middleware da API.
"""

from .auth import verify_token

__all__ = ["verify_token"]