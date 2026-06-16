"""Authentication backends for password and API-key credentials."""

from __future__ import annotations

from collections.abc import Mapping
from datetime import datetime, timezone
from typing import Any, Iterable

from tigrbl_identity_jose.key_management import verify_pw
from tigrbl_identity_core.typing import Principal
from tigrbl_identity_storage.tables import ApiKey, Client, ServiceKey, User


class AuthError(Exception):
    def __init__(self, reason: str = "authentication failed"):
        super().__init__(reason)
        self.reason = reason


def _list_items(result: Any) -> list[Any]:
    if isinstance(result, Mapping) and isinstance(result.get("items"), list):
        result = result["items"]
    elif hasattr(result, "items"):
        result = result.items
    if isinstance(result, list):
        return result
    if isinstance(result, tuple):
        return list(result)
    if result is None:
        return []
    return [result]


def _value_matches(actual: Any, expected: Any) -> bool:
    if actual == expected:
        return True
    if actual is None or expected is None:
        return False
    return str(actual) == str(expected)


def _active(row: Any) -> bool:
    return bool(getattr(row, "is_active", True))


def _valid_now(row: Any) -> bool:
    now = datetime.now(timezone.utc)
    valid_from = getattr(row, "valid_from", None)
    valid_to = getattr(row, "valid_to", None)
    if isinstance(valid_from, datetime):
        if getattr(valid_from, "tzinfo", None) is None:
            valid_from = valid_from.replace(tzinfo=timezone.utc)
        if valid_from > now:
            return False
    if isinstance(valid_to, datetime):
        if getattr(valid_to, "tzinfo", None) is None:
            valid_to = valid_to.replace(tzinfo=timezone.utc)
        if valid_to <= now:
            return False
    return True


async def _handler_rows(model: Any, db: Any, filters: Mapping[str, Any] | None = None) -> list[Any]:
    payload = {"filters": dict(filters or {})}
    return _list_items(await model.handlers.list.core({"payload": payload, "db": db}))


async def _first_handler_record(model: Any, db: Any, filters: Mapping[str, Any]) -> Any:
    for row in await _handler_rows(model, db, filters):
        if all(not hasattr(row, key) or _value_matches(getattr(row, key, None), value) for key, value in filters.items()):
            return row
    return None


class PasswordBackend:
    async def _get_user_candidates(self, db: Any, identifier: str) -> list[User]:
        rows = await _handler_rows(User, db, {"is_active": True})
        return [
            row
            for row in rows
            if _active(row)
            and (_value_matches(getattr(row, "username", None), identifier) or _value_matches(getattr(row, "email", None), identifier))
        ]

    async def authenticate(self, db: Any, identifier: str, password: str) -> User:
        row = next(iter(await self._get_user_candidates(db, identifier)), None)
        if not row or not verify_pw(password, row.password_hash):
            raise AuthError("invalid username/email or password")
        return row


class ApiKeyBackend:
    async def _get_key_row(self, db: Any, digest: str) -> ApiKey | None:
        row = await _first_handler_record(ApiKey, db, {"digest": digest})
        return row if row is not None and _valid_now(row) else None

    async def _get_service_key_row(self, db: Any, digest: str) -> ServiceKey | None:
        row = await _first_handler_record(ServiceKey, db, {"digest": digest})
        return row if row is not None and _valid_now(row) else None

    async def _get_client_rows(self, db: Any) -> list[Client]:
        return [row for row in await _handler_rows(Client, db, {"is_active": True}) if _active(row)]

    async def authenticate(self, db: Any, api_key: str) -> tuple[Principal, str]:
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

        clients: Iterable[Client] = await self._get_client_rows(db)
        for client in clients:
            if client.verify_secret(api_key):
                return client, "client"

        raise AuthError("API key invalid, revoked, or expired")


__all__ = ["AuthError", "PasswordBackend", "ApiKeyBackend"]
