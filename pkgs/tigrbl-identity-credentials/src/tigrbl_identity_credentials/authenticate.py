"""Legacy import facade for canonical authentication backend operations.

The authoritative implementations live in ``tigrbl_identity_credentials.backends``.
"""

from tigrbl_identity_credentials.backends import ApiKeyBackend, AuthError, PasswordBackend

__all__ = ["ApiKeyBackend", "AuthError", "PasswordBackend"]
