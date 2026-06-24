"""Durable dynamic client registration metadata."""

from __future__ import annotations

import datetime as dt
from typing import Any

from tigrbl_identity_storage.framework import (
    RestOltpTable,
    BaseModel,
    EmailStr,
    Field,
    TenantColumn,
    Timestamped,
    S,
    acol,
    JSON,
    Mapped,
    String,
    TZDateTime,
    GUIDPk,
    ForeignKeySpec,
    PgUUID,
    UUID,
    constr,
)
from .._ops import create_record, delete_record, first_record, record_id, update_record, utc_now

_tenant_slug = constr(strip_whitespace=True, min_length=3, max_length=120)


class DynamicClientRegistrationIn(BaseModel):
    tenant_slug: _tenant_slug = Field(default="public")
    redirect_uris: list[str]
    grant_types: list[str] = Field(default_factory=lambda: ["authorization_code"])
    response_types: list[str] = Field(default_factory=lambda: ["code"])
    token_endpoint_auth_method: str = Field(default="client_secret_basic")
    token_endpoint_auth_signing_alg: str | None = None
    tls_client_certificate_thumbprint: str | None = None
    self_signed_tls_client_certificate_thumbprint: str | None = None
    tls_client_auth_subject_dn: str | None = None
    tls_client_auth_san_dns: str | None = None
    tls_client_auth_san_uri: str | None = None
    tls_client_auth_san_ip: str | None = None
    tls_client_auth_san_email: str | None = None
    application_type: str | None = None
    scope: str | None = None
    client_name: str | None = None
    client_uri: str | None = None
    jwks_uri: str | None = None
    contacts: list[EmailStr] | None = None
    software_id: str | None = None
    software_version: str | None = None
    post_logout_redirect_uris: list[str] | None = None
    frontchannel_logout_uri: str | None = None
    frontchannel_logout_session_required: bool = True
    backchannel_logout_uri: str | None = None
    backchannel_logout_session_required: bool = True


class DynamicClientRegistrationOut(BaseModel):
    client_id: str
    client_secret: str | None = None
    client_id_issued_at: int
    client_secret_expires_at: int = 0
    redirect_uris: list[str]
    grant_types: list[str]
    response_types: list[str]
    token_endpoint_auth_method: str
    token_endpoint_auth_signing_alg: str | None = None
    tls_client_certificate_thumbprint: str | None = None
    self_signed_tls_client_certificate_thumbprint: str | None = None
    tls_client_auth_subject_dn: str | None = None
    tls_client_auth_san_dns: str | None = None
    tls_client_auth_san_uri: str | None = None
    tls_client_auth_san_ip: str | None = None
    tls_client_auth_san_email: str | None = None
    application_type: str | None = None
    scope: str | None = None
    client_name: str | None = None
    client_uri: str | None = None
    jwks_uri: str | None = None
    contacts: list[EmailStr] | None = None
    software_id: str | None = None
    software_version: str | None = None
    post_logout_redirect_uris: list[str] | None = None
    frontchannel_logout_uri: str | None = None
    frontchannel_logout_session_required: bool = True
    backchannel_logout_uri: str | None = None
    backchannel_logout_session_required: bool = True
    registration_access_token: str | None = None
    registration_client_uri: str | None = None


class DynamicClientRegistrationManagementIn(BaseModel):
    tenant_slug: _tenant_slug | None = None
    redirect_uris: list[str] | None = None
    grant_types: list[str] | None = None
    response_types: list[str] | None = None
    token_endpoint_auth_method: str | None = None
    token_endpoint_auth_signing_alg: str | None = None
    tls_client_certificate_thumbprint: str | None = None
    self_signed_tls_client_certificate_thumbprint: str | None = None
    tls_client_auth_subject_dn: str | None = None
    tls_client_auth_san_dns: str | None = None
    tls_client_auth_san_uri: str | None = None
    tls_client_auth_san_ip: str | None = None
    tls_client_auth_san_email: str | None = None
    application_type: str | None = None
    scope: str | None = None
    client_name: str | None = None
    client_uri: str | None = None
    jwks_uri: str | None = None
    contacts: list[EmailStr] | None = None
    software_id: str | None = None
    software_version: str | None = None
    post_logout_redirect_uris: list[str] | None = None
    frontchannel_logout_uri: str | None = None
    frontchannel_logout_session_required: bool | None = None
    backchannel_logout_uri: str | None = None
    backchannel_logout_session_required: bool | None = None


class ClientRegistration(RestOltpTable, GUIDPk, Timestamped, TenantColumn):
    __tablename__ = "client_registrations"
    __table_args__ = ({"schema": "authn"},)

    client_id: Mapped[UUID] = acol(
        storage=S(PgUUID(as_uuid=True), fk=ForeignKeySpec(target="authn.clients.id"), nullable=False, unique=True, index=True)
    )
    software_id: Mapped[str | None] = acol(storage=S(String(255), nullable=True, index=True))
    software_version: Mapped[str | None] = acol(storage=S(String(128), nullable=True))
    contacts: Mapped[list[str] | None] = acol(storage=S(JSON, nullable=True))
    registration_metadata: Mapped[dict[str, Any] | None] = acol(storage=S(JSON, nullable=True))
    registration_access_token_hash: Mapped[str | None] = acol(
        storage=S(String(128), nullable=True, unique=True, index=True)
    )
    registration_client_uri: Mapped[str | None] = acol(storage=S(String(1000), nullable=True))
    issued_at: Mapped[dt.datetime] = acol(
        storage=S(TZDateTime, nullable=False, default=lambda: dt.datetime.now(dt.timezone.utc))
    )
    rotated_at: Mapped[dt.datetime | None] = acol(storage=S(TZDateTime, nullable=True))
    disabled_at: Mapped[dt.datetime | None] = acol(storage=S(TZDateTime, nullable=True, index=True))


__all__ = [
    "ClientRegistration",
    "DynamicClientRegistrationIn",
    "DynamicClientRegistrationManagementIn",
    "DynamicClientRegistrationOut",
]
