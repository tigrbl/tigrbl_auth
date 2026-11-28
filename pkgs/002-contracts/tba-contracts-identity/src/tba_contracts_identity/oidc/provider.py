"""OpenID Provider contract ports."""

from __future__ import annotations

from typing import Any, Mapping, Protocol

from .discovery import DiscoveryDocumentRequest
from .userinfo import UserInfoRequest, UserInfoResult


class IdTokenIssuerPort(Protocol):
    async def issue_id_token(self, claims: Mapping[str, Any], /) -> str: ...


class IdTokenVerifierPort(Protocol):
    async def verify_id_token(self, token: str, /) -> Mapping[str, Any]: ...


class OpenIDProviderPort(IdTokenIssuerPort, IdTokenVerifierPort, Protocol):
    async def discovery_document(
        self, request: DiscoveryDocumentRequest, /
    ) -> Mapping[str, Any]: ...

    async def userinfo(self, request: UserInfoRequest, /) -> UserInfoResult: ...


__all__ = [
    "DiscoveryDocumentRequest",
    "IdTokenIssuerPort",
    "IdTokenVerifierPort",
    "OpenIDProviderPort",
    "UserInfoRequest",
    "UserInfoResult",
]
