"""Legacy import facade for canonical authentication backend implementations.

The authoritative implementations live in ``tigrbl_auth.services.auth_backends``.
This module remains only to preserve existing import sites during the migration
window without relying on star-import shims.
"""

from tigrbl_auth.services.auth_backends import ApiKeyBackend, AuthError, PasswordBackend
from tigrbl_auth.tables import ApiKey as _ApiKey


__all__ = ["ApiKeyBackend", "AuthError", "PasswordBackend", "_ApiKey"]
