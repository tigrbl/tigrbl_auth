"""Legacy import facade for canonical authentication backend operations.

The authoritative implementations live in ``tba_credentials.backends``.
"""

from tba_credentials.backends import ApiKeyBackend, AuthError, PasswordBackend

__all__ = ["ApiKeyBackend", "AuthError", "PasswordBackend"]
