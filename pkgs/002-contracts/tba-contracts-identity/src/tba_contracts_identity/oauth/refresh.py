"""OAuth refresh-token lifecycle contracts."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Mapping, Protocol


@dataclass(frozen=True, slots=True)
class RefreshTokenRequest:
    refresh_token: str
    scopes: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class IssuedTokenSet:
    access_token: str
    token_type: str = "Bearer"
    expires_in: int | None = None
    refresh_token: str | None = None
    id_token: str | None = None


@dataclass(frozen=True, slots=True)
class TokenRecord:
    token_hash: str
    token_kind: str
    claims: Mapping[str, Any] = field(default_factory=dict)
    token_type_hint: str | None = None
    expires_at: datetime | None = None
    revoked_at: datetime | None = None


class RefreshTokenLifecyclePort(Protocol):
    async def redeem(
        self,
        request: RefreshTokenRequest,
        /,
        *,
        client_id: str | None = None,
        audience: tuple[str, ...] = (),
    ) -> IssuedTokenSet: ...

    async def persist_issued(
        self,
        *,
        token_hash: str,
        claims: Mapping[str, Any],
        token_kind: str,
        token_type_hint: str | None = None,
    ) -> TokenRecord: ...


__all__ = [
    "IssuedTokenSet",
    "RefreshTokenLifecyclePort",
    "RefreshTokenRequest",
    "TokenRecord",
]
