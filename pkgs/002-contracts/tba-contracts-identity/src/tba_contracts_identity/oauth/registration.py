"""Carrier-neutral dynamic client registration contracts."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Mapping, Protocol


@dataclass(frozen=True, slots=True)
class ClientRegistrationCreateRequest:
    """Normalized durable input for creating a client registration."""

    client_id: str
    tenant_id: str
    client_secret_hash: str
    redirect_uris: tuple[str, ...]
    grant_types: tuple[str, ...] = ("authorization_code",)
    response_types: tuple[str, ...] = ("code",)
    metadata: Mapping[str, object] = field(default_factory=dict)
    contacts: tuple[str, ...] = ()
    software_id: str | None = None
    software_version: str | None = None
    registration_access_token_hash: str | None = None
    registration_client_uri: str | None = None

    def __post_init__(self) -> None:
        if not self.client_id:
            raise ValueError("client_id is required")
        if not self.tenant_id:
            raise ValueError("tenant_id is required")
        if not self.client_secret_hash:
            raise ValueError("client_secret_hash is required")
        if not self.redirect_uris:
            raise ValueError("at least one redirect_uri is required")


@dataclass(frozen=True, slots=True)
class ClientRegistrationUpdateRequest:
    """Normalized durable input for replacing mutable registration metadata."""

    client_id: str
    redirect_uris: tuple[str, ...]
    grant_types: tuple[str, ...]
    response_types: tuple[str, ...]
    metadata: Mapping[str, object]
    contacts: tuple[str, ...] = ()
    software_id: str | None = None
    software_version: str | None = None
    updated_fields: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.client_id:
            raise ValueError("client_id is required")
        if not self.redirect_uris:
            raise ValueError("at least one redirect_uri is required")


@dataclass(frozen=True, slots=True)
class ClientRegistrationRecord:
    """Protocol-neutral view of one durable client-registration aggregate."""

    client_id: str
    tenant_id: str
    registration_id: str
    redirect_uris: tuple[str, ...]
    grant_types: tuple[str, ...]
    response_types: tuple[str, ...]
    metadata: Mapping[str, object]
    contacts: tuple[str, ...] = ()
    software_id: str | None = None
    software_version: str | None = None
    registration_access_token_hash: str | None = None
    registration_client_uri: str | None = None
    issued_at: datetime | None = None
    disabled_at: datetime | None = None
    client_active: bool = True


class ClientRegistrationPort(Protocol):
    """Durable operations consumed by registration capabilities."""

    async def create(
        self, request: ClientRegistrationCreateRequest, /
    ) -> ClientRegistrationRecord: ...

    async def get(self, client_id: str, /) -> ClientRegistrationRecord | None: ...

    async def update(
        self, request: ClientRegistrationUpdateRequest, /
    ) -> ClientRegistrationRecord: ...

    async def disable(self, client_id: str, /) -> ClientRegistrationRecord: ...


__all__ = [
    "ClientRegistrationCreateRequest",
    "ClientRegistrationPort",
    "ClientRegistrationRecord",
    "ClientRegistrationUpdateRequest",
]
