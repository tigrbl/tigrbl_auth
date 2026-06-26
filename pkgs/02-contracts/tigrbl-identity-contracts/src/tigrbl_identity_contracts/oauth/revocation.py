"""OAuth token revocation contracts backed by revoked-token schemas."""

from __future__ import annotations

from typing import Protocol

from ..schemas import RevocationIn, RevocationOut, RevokedTokenReadResponse


class TokenRevocationPort(Protocol):
    async def revoke(self, request: RevocationIn, /) -> RevocationOut: ...

    async def record_hash(
        self,
        *,
        token_hash: str,
        token_type_hint: str | None = None,
        reason: str | None = None,
    ) -> RevokedTokenReadResponse: ...

    async def is_hash_revoked(self, *, token_hash: str) -> bool: ...


__all__ = ["RevocationIn", "RevocationOut", "RevokedTokenReadResponse", "TokenRevocationPort"]
