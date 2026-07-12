"""OIDC discovery publisher contracts."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping, Protocol

from ..schemas import AuthorizationServerReadResponse, RealmReadResponse


@dataclass(frozen=True, slots=True)
class DiscoveryDocumentRequest:
    issuer: str
    authorization_server: AuthorizationServerReadResponse | None = None
    realm: RealmReadResponse | None = None
    context: Mapping[str, Any] = field(default_factory=dict)


class DiscoveryPublisherPort(Protocol):
    async def discovery_document(
        self, request: DiscoveryDocumentRequest, /
    ) -> Mapping[str, Any]: ...


__all__ = [
    "AuthorizationServerReadResponse",
    "DiscoveryDocumentRequest",
    "DiscoveryPublisherPort",
    "RealmReadResponse",
]
