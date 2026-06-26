"""Durable authorization-server configuration and metadata state."""

from __future__ import annotations

import uuid

from tigrbl_identity_storage.framework import (
    ForeignKeySpec,
    GUIDPk,
    JSON,
    Mapped,
    PgUUID,
    RestOltpTable,
    S,
    String,
    Timestamped,
    acol,
)


class AuthorizationServer(RestOltpTable, GUIDPk, Timestamped):
    __tablename__ = "authorization_servers"
    __table_args__ = ({"schema": "authn"},)

    issuer: Mapped[str] = acol(storage=S(String(512), nullable=False, unique=True, index=True))
    tenant_id: Mapped[uuid.UUID | None] = acol(
        storage=S(
            PgUUID(as_uuid=True),
            fk=ForeignKeySpec(target="authn.tenants.id"),
            nullable=True,
            index=True,
        )
    )
    realm_id: Mapped[uuid.UUID | None] = acol(
        storage=S(
            PgUUID(as_uuid=True),
            fk=ForeignKeySpec(target="authn.realms.id"),
            nullable=True,
            index=True,
        )
    )
    status: Mapped[str] = acol(storage=S(String(64), nullable=False, default="active", index=True))
    authorization_endpoint: Mapped[str | None] = acol(storage=S(String(512), nullable=True))
    token_endpoint: Mapped[str | None] = acol(storage=S(String(512), nullable=True))
    jwks_uri: Mapped[str | None] = acol(storage=S(String(512), nullable=True))
    introspection_endpoint: Mapped[str | None] = acol(storage=S(String(512), nullable=True))
    revocation_endpoint: Mapped[str | None] = acol(storage=S(String(512), nullable=True))
    registration_endpoint: Mapped[str | None] = acol(storage=S(String(512), nullable=True))
    userinfo_endpoint: Mapped[str | None] = acol(storage=S(String(512), nullable=True))
    server_metadata: Mapped[dict | None] = acol(storage=S(JSON, nullable=True))
    oauth_metadata: Mapped[dict | None] = acol(storage=S(JSON, nullable=True))
    oidc_metadata: Mapped[dict | None] = acol(storage=S(JSON, nullable=True))
    scopes_supported: Mapped[list | None] = acol(storage=S(JSON, nullable=True))
    response_types_supported: Mapped[list | None] = acol(storage=S(JSON, nullable=True))
    grant_types_supported: Mapped[list | None] = acol(storage=S(JSON, nullable=True))
    token_endpoint_auth_methods_supported: Mapped[list | None] = acol(storage=S(JSON, nullable=True))
    subject_types_supported: Mapped[list | None] = acol(storage=S(JSON, nullable=True))
    signing_alg_values_supported: Mapped[list | None] = acol(storage=S(JSON, nullable=True))


__all__ = ["AuthorizationServer"]
