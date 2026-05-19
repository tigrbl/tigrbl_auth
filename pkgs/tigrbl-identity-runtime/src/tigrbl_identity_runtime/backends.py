"""Legacy import facade for canonical authentication backend implementations.

The authoritative implementations live in ``tigrbl_auth.services.auth_backends``.
This module remains only to preserve existing import sites during the migration
window without relying on star-import shims.
"""

from tigrbl_auth.services.auth_backends import ApiKeyBackend as _ApiKeyBackend, AuthError, PasswordBackend
from tigrbl_auth.tables import ApiKey as _ApiKey


class ApiKeyBackend(_ApiKeyBackend):
    async def authenticate(self, db, api_key):
        # Preserve legacy patch point used by unit tests.
        digest = _ApiKey().digest_of(api_key)

        key_row = await db.scalar(await self._get_key_stmt(digest))
        user = getattr(key_row, "user", None) or getattr(key_row, "_user", None)
        if key_row and user:
            if not user.is_active:
                raise AuthError("user is inactive")
            key_row.touch()
            return user, "user"

        svc_row = await db.scalar(await self._get_service_key_stmt(digest))
        service = getattr(svc_row, "service", None) or getattr(svc_row, "_service", None)
        if svc_row and service:
            if not service.is_active:
                raise AuthError("service is inactive")
            svc_row.touch()
            return service, "service"

        clients = await db.scalars(await self._get_client_stmt())
        for client in clients:
            if client.verify_secret(api_key):
                return client, "client"

        raise AuthError("API key invalid, revoked, or expired")


__all__ = ["ApiKeyBackend", "AuthError", "PasswordBackend", "_ApiKey"]
