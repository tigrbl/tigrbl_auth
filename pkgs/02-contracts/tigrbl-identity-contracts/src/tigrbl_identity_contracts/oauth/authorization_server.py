"""Authorization-server configuration contracts backed by storage schemas."""

from __future__ import annotations

from typing import Any, Mapping, Protocol

from ..schemas import (
    AuthorizationServerCreateRequest,
    AuthorizationServerReadResponse,
    AuthorizationServerUpdateRequest,
)


class AuthorizationServerResolverPort(Protocol):
    async def get_by_issuer(self, issuer: str, /) -> AuthorizationServerReadResponse | None: ...

    async def list_active(
        self,
        *,
        tenant_id: str | None = None,
        realm_id: str | None = None,
    ) -> tuple[AuthorizationServerReadResponse, ...]: ...


class AuthorizationServerMetadataPublisherPort(Protocol):
    async def publish_metadata(
        self,
        server: AuthorizationServerReadResponse,
        /,
    ) -> Mapping[str, Any]: ...


class AuthorizationServerConfigPort(
    AuthorizationServerResolverPort,
    AuthorizationServerMetadataPublisherPort,
    Protocol,
):
    async def create(
        self,
        request: AuthorizationServerCreateRequest,
        /,
    ) -> AuthorizationServerReadResponse: ...

    async def update(
        self,
        server_id: str,
        request: AuthorizationServerUpdateRequest,
        /,
    ) -> AuthorizationServerReadResponse: ...


__all__ = [
    "AuthorizationServerConfigPort",
    "AuthorizationServerCreateRequest",
    "AuthorizationServerMetadataPublisherPort",
    "AuthorizationServerReadResponse",
    "AuthorizationServerResolverPort",
    "AuthorizationServerUpdateRequest",
]
