"""OIDC relying-party contract ports."""

from __future__ import annotations

from typing import Any, Mapping, Protocol


class RelyingPartyPort(Protocol):
    async def build_authorization_request(
        self, *, state: str, nonce: str, scope: str
    ) -> Mapping[str, Any]: ...

    async def handle_callback(
        self, params: Mapping[str, Any], /
    ) -> Mapping[str, Any]: ...


__all__ = ["RelyingPartyPort"]
