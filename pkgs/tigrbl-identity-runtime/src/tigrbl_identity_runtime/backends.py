"""Legacy import facade for canonical authentication backend implementations.

The authoritative implementations live in ``tigrbl_authn_credentials.backends``.
This module remains only to preserve existing import sites during the migration
window without relying on star-import shims.
"""

from tigrbl_authn_credentials.backends import ApiKeyBackend, AuthError, PasswordBackend
from tigrbl_identity_storage.tables import ApiKey as _ApiKey


__all__ = ["ApiKeyBackend", "AuthError", "PasswordBackend", "_ApiKey"]
