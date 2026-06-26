"""OAuth consent service contracts backed by storage table schemas."""

from __future__ import annotations

from typing import Protocol

from ..schemas import ConsentCreateRequest, ConsentReadResponse, ConsentUpdateRequest


class ConsentServicePort(Protocol):
    async def grant(self, request: ConsentCreateRequest, /) -> ConsentReadResponse: ...

    async def list_for_user(
        self,
        *,
        user_id: str,
        tenant_id: str | None = None,
    ) -> tuple[ConsentReadResponse, ...]: ...

    async def revoke(self, request: ConsentUpdateRequest, /) -> ConsentReadResponse | None: ...

    async def revoke_for_client(
        self,
        *,
        client_id: str,
        user_id: str | None = None,
        tenant_id: str | None = None,
    ) -> tuple[ConsentReadResponse, ...]: ...


__all__ = ["ConsentCreateRequest", "ConsentReadResponse", "ConsentServicePort", "ConsentUpdateRequest"]
