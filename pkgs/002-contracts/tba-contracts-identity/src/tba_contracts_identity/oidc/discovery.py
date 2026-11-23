"""OIDC discovery publisher contracts."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping, Protocol

from ..oauth.authorization_server import AuthorizationServerConfiguration


@dataclass(frozen=True, slots=True)
class RealmDescriptor:
    realm_id: str
    slug: str
    name: str
    issuer_path: str
    description: str | None = None


@dataclass(frozen=True, slots=True)
class DiscoveryDocumentRequest:
    issuer: str
    authorization_server: AuthorizationServerConfiguration | None = None
    realm: RealmDescriptor | None = None
    context: Mapping[str, Any] = field(default_factory=dict)


class DiscoveryPublisherPort(Protocol):
    async def discovery_document(
        self, request: DiscoveryDocumentRequest, /
    ) -> Mapping[str, Any]: ...


__all__ = [
    "AuthorizationServerConfiguration",
    "DiscoveryDocumentRequest",
    "DiscoveryPublisherPort",
    "RealmDescriptor",
]
