"""OAuth refresh-token lifecycle contracts backed by token-record schemas."""

from __future__ import annotations

from typing import Any, Mapping, Protocol

from ..schemas import RefreshIn, TokenPair, TokenRecordReadResponse


class RefreshTokenLifecyclePort(Protocol):
    async def redeem(
        self,
        request: RefreshIn,
        /,
        *,
        client_id: str | None = None,
        audience: tuple[str, ...] = (),
    ) -> TokenPair: ...

    async def persist_issued(
        self,
        *,
        token_hash: str,
        claims: Mapping[str, Any],
        token_kind: str,
        token_type_hint: str | None = None,
    ) -> TokenRecordReadResponse: ...


__all__ = ["RefreshIn", "RefreshTokenLifecyclePort", "TokenPair", "TokenRecordReadResponse"]
