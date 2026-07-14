"""Authentication backends for password and API-key credentials."""

from __future__ import annotations

from datetime import datetime, timezone
import inspect
from collections.abc import Awaitable, Callable, Sequence
from typing import Any

from tigrbl_identity_jose.key_management import verify_pw
from tigrbl_identity_contracts.principals import PrincipalLike

Lookup = Callable[[Any, str], Awaitable[Sequence[Any]]]
ResolvePrincipal = Callable[[Any, Any], Awaitable[Any | None]]
MarkUsed = Callable[[Any, Any], object | Awaitable[object]]


class AuthError(Exception):
    def __init__(self, reason: str = "authentication failed"):
        super().__init__(reason)
        self.reason = reason


def _active(row: Any) -> bool:
    return bool(getattr(row, "is_active", True))


def _field(row: Any, key: str, default: Any = None) -> Any:
    if isinstance(row, dict):
        return row.get(key, default)
    return getattr(row, key, default)


async def _maybe_await(value: object | Awaitable[object]) -> object:
    if inspect.isawaitable(value):
        return await value
    return value


class PasswordBackend:
    def __init__(self, *, find_principals: Lookup) -> None:
        self._find_principals = find_principals

    async def _get_user_candidates(self, db: Any, identifier: str) -> list[Any]:
        rows = await self._find_principals(db, identifier)
        return [row for row in rows if _active(row)]

    async def authenticate(self, db: Any, identifier: str, password: str) -> Any:
        row = next(iter(await self._get_user_candidates(db, identifier)), None)
        if not row or not verify_pw(password, row.password_hash):
            raise AuthError("invalid username/email or password")
        return row


class ApiKeyBackend:
    def __init__(
        self,
        *,
        digest_key: Callable[[str], str],
        find_api_keys: Lookup,
        find_service_keys: Lookup,
        resolve_user: ResolvePrincipal,
        mark_used: MarkUsed,
    ) -> None:
        self._digest_key = digest_key
        self._find_api_keys = find_api_keys
        self._find_service_keys = find_service_keys
        self._resolve_user = resolve_user
        self._mark_used = mark_used

    async def _get_key_row(self, db: Any, digest: str) -> Any | None:
        return self._valid_key(await self._find_api_keys(db, digest))

    async def _get_service_key_row(
        self, db: Any, digest: str
    ) -> Any | None:
        return self._valid_key(await self._find_service_keys(db, digest))

    @staticmethod
    def _valid_key(rows: list[Any]):
        now = datetime.now(timezone.utc)
        for row in rows:
            status_value = _field(row, "status", "active")
            if isinstance(status_value, str) and status_value != "active":
                continue
            valid_from = _field(row, "valid_from")
            valid_to = _field(row, "valid_to")
            if isinstance(valid_from, datetime) and valid_from > now:
                continue
            if isinstance(valid_to, datetime) and valid_to <= now:
                continue
            return row
        return None

    async def authenticate(self, db: Any, api_key: str) -> tuple[PrincipalLike, str]:
        digest = self._digest_key(api_key)

        key_row = await self._get_key_row(db, digest)
        user = (
            await self._resolve_user(db, key_row)
            if key_row is not None
            else None
        )
        if key_row and user:
            if not user.is_active:
                raise AuthError("user is inactive")
            await _maybe_await(self._mark_used(db, key_row))
            return user, "user"

        svc_row = await self._get_service_key_row(db, digest)
        service_identity = (
            getattr(svc_row, "service_identity", None)
            or getattr(svc_row, "_service_identity", None)
            or getattr(svc_row, "service", None)
            or getattr(svc_row, "_service", None)
        )
        if svc_row and service_identity:
            if not service_identity.is_active:
                raise AuthError("service identity is inactive")
            await _maybe_await(self._mark_used(db, svc_row))
            return service_identity, "service_identity"

        raise AuthError("API key invalid, revoked, or expired")


__all__ = ["AuthError", "PasswordBackend", "ApiKeyBackend"]
