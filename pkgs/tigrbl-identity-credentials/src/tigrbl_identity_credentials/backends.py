"""Authentication backends for password and API-key credentials."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Iterable, Optional

from tigrbl_auth.framework import Select, or_, select, AsyncSession
from tigrbl_auth.services.key_management import verify_pw
from tigrbl_auth.typing import Principal
from tigrbl_auth.tables import ApiKey, Client, ServiceKey, User


class AuthError(Exception):
    def __init__(self, reason: str = "authentication failed"):
        super().__init__(reason)
        self.reason = reason


class PasswordBackend:
    async def _get_user_stmt(self, identifier: str) -> Select[tuple[User]]:
        return select(User).where(
            or_(User.username == identifier, User.email == identifier),
            User.is_active.is_(True),
        )

    async def authenticate(self, db: AsyncSession, identifier: str, password: str) -> User:
        row: Optional[User] = await db.scalar(await self._get_user_stmt(identifier))
        if not row or not verify_pw(password, row.password_hash):
            raise AuthError("invalid username/email or password")
        return row


class ApiKeyBackend:
    async def _get_key_stmt(self, digest: str) -> Select[tuple[ApiKey]]:
        now = datetime.now(timezone.utc)
        return select(ApiKey).where(
            ApiKey.digest == digest,
            or_(ApiKey.valid_to.is_(None), ApiKey.valid_to > now),
        )

    async def _get_service_key_stmt(self, digest: str) -> Select[tuple[ServiceKey]]:
        now = datetime.now(timezone.utc)
        return select(ServiceKey).where(
            ServiceKey.digest == digest,
            or_(ServiceKey.valid_to.is_(None), ServiceKey.valid_to > now),
        )

    async def _get_client_stmt(self) -> Select[tuple[Client]]:
        return select(Client).where(Client.is_active.is_(True))

    async def authenticate(self, db: AsyncSession, api_key: str) -> tuple[Principal, str]:
        digest = ApiKey.digest_of(api_key)

        key_row: Optional[ApiKey] = await db.scalar(await self._get_key_stmt(digest))
        user = getattr(key_row, "user", None) or getattr(key_row, "_user", None)
        if key_row and user:
            if not user.is_active:
                raise AuthError("user is inactive")
            key_row.touch()
            return user, "user"

        svc_row: Optional[ServiceKey] = await db.scalar(await self._get_service_key_stmt(digest))
        service = getattr(svc_row, "service", None) or getattr(svc_row, "_service", None)
        if svc_row and service:
            if not service.is_active:
                raise AuthError("service is inactive")
            svc_row.touch()
            return service, "service"

        clients: Iterable[Client] = await db.scalars(await self._get_client_stmt())
        for client in clients:
            if client.verify_secret(api_key):
                return client, "client"

        raise AuthError("API key invalid, revoked, or expired")


__all__ = ["AuthError", "PasswordBackend", "ApiKeyBackend"]
