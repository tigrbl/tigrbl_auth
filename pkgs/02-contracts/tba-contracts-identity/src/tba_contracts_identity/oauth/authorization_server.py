"""Authorization-server configuration contracts."""

from __future__ import annotations

from dataclasses import dataclass, field, replace
from typing import Any, Mapping, Protocol


@dataclass(frozen=True, slots=True)
class AuthorizationServerConfiguration:
    issuer: str
    server_id: str | None = None
    tenant_id: str | None = None
    realm_id: str | None = None
    status: str = "active"
    authorization_endpoint: str | None = None
    token_endpoint: str | None = None
    jwks_uri: str | None = None
    introspection_endpoint: str | None = None
    revocation_endpoint: str | None = None
    registration_endpoint: str | None = None
    userinfo_endpoint: str | None = None
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def with_changes(self, **changes: Any) -> "AuthorizationServerConfiguration":
        return replace(self, **changes)


@dataclass(frozen=True, slots=True)
class AuthorizationServerPatch:
    values: Mapping[str, Any]


class AuthorizationServerResolverPort(Protocol):
    async def get_by_issuer(
        self, issuer: str, /
    ) -> AuthorizationServerConfiguration | None: ...

    async def list_active(
        self,
        *,
        tenant_id: str | None = None,
        realm_id: str | None = None,
    ) -> tuple[AuthorizationServerConfiguration, ...]: ...


class AuthorizationServerMetadataPublisherPort(Protocol):
    async def publish_metadata(
        self,
        server: AuthorizationServerConfiguration,
        /,
    ) -> Mapping[str, Any]: ...


class AuthorizationServerConfigPort(
    AuthorizationServerResolverPort,
    AuthorizationServerMetadataPublisherPort,
    Protocol,
):
    async def create(
        self,
        request: AuthorizationServerConfiguration,
        /,
    ) -> AuthorizationServerConfiguration: ...

    async def update(
        self,
        server_id: str,
        request: AuthorizationServerPatch,
        /,
    ) -> AuthorizationServerConfiguration: ...


__all__ = [
    "AuthorizationServerConfigPort",
    "AuthorizationServerConfiguration",
    "AuthorizationServerMetadataPublisherPort",
    "AuthorizationServerResolverPort",
    "AuthorizationServerPatch",
]
