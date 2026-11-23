"""OAuth token revocation contracts."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Protocol


@dataclass(frozen=True, slots=True)
class TokenRevocationRequest:
    token: str
    token_type_hint: str | None = None
    reason: str | None = None


@dataclass(frozen=True, slots=True)
class TokenRevocationResult:
    revoked: bool


@dataclass(frozen=True, slots=True)
class RevokedTokenRecord:
    token_hash: str
    token_type_hint: str | None = None
    reason: str | None = None
    revoked_at: datetime | None = None
    expires_at: datetime | None = None


class TokenRevocationPort(Protocol):
    async def revoke(
        self, request: TokenRevocationRequest, /
    ) -> TokenRevocationResult: ...

    async def record_hash(
        self,
        *,
        token_hash: str,
        token_type_hint: str | None = None,
        reason: str | None = None,
    ) -> RevokedTokenRecord: ...

    async def is_hash_revoked(self, *, token_hash: str) -> bool: ...


__all__ = [
    "RevokedTokenRecord",
    "TokenRevocationPort",
    "TokenRevocationRequest",
    "TokenRevocationResult",
]
