"""Authentication backends for password and API-key credentials."""

from __future__ import annotations

from typing import Any

from tigrbl_identity_jose.key_management import verify_pw
from tigrbl_identity_contracts.principals import PrincipalLike
from tigrbl_identity_storage.tables import ApiKey, Client, ServiceKey, User


class AuthError(Exception):
    def __init__(self, reason: str = "authentication failed"):
        super().__init__(reason)
        self.reason = reason


def _active(row: Any) -> bool:
    return bool(getattr(row, "is_active", True))


class PasswordBackend:
    async def _get_user_candidates(self, db: Any, identifier: str) -> list[User]:
        row = await User.lookup_by_identifier(db, identifier=identifier)
        return [row] if row is not None and _active(row) else []

    async def authenticate(self, db: Any, identifier: str, password: str) -> User:
        row = next(iter(await self._get_user_candidates(db, identifier)), None)
        if not row or not verify_pw(password, row.password_hash):
            raise AuthError("invalid username/email or password")
        return row


class ApiKeyBackend:
    async def _get_key_row(self, db: Any, digest: str) -> ApiKey | None:
        return await ApiKey.lookup_active(db, digest=digest)

    async def _get_service_key_row(self, db: Any, digest: str) -> ServiceKey | None:
        return await ServiceKey.lookup_active(db, digest=digest)

    async def authenticate(self, db: Any, api_key: str) -> tuple[PrincipalLike, str]:
        digest = ApiKey.digest_of(api_key)

        key_row = await self._get_key_row(db, digest)
        user = getattr(key_row, "user", None) or getattr(key_row, "_user", None)
        if key_row and user:
            if not user.is_active:
                raise AuthError("user is inactive")
            key_row.touch()
            return user, "user"

        svc_row = await self._get_service_key_row(db, digest)
        service = getattr(svc_row, "service", None) or getattr(svc_row, "_service", None)
        if svc_row and service:
            if not service.is_active:
                raise AuthError("service is inactive")
            svc_row.touch()
            return service, "service"

        client = await Client.authenticate(db, client_secret=api_key)
        if client is not None:
            return client, "client"

        raise AuthError("API key invalid, revoked, or expired")


__all__ = ["AuthError", "PasswordBackend", "ApiKeyBackend"]
