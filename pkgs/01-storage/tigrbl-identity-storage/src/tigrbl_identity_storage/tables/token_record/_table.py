"""Durable token status and introspection backing store."""

from __future__ import annotations

import datetime as dt
import uuid
from typing import Literal, Optional

from tigrbl_identity_storage.framework import (
    RestOltpTable,
    BaseModel,
    Field,
    Timestamped,
    S,
    acol,
    JSON,
    Boolean,
    Mapped,
    String,
    TZDateTime,
    GUIDPk,
    ForeignKeySpec,
    PgUUID,
    Integer,
)
from tigrbl_identity_core.typing import StrUUID


class TokenPair(BaseModel):
    access_token: str
    refresh_token: Optional[str] = None
    token_type: str = Field(default="bearer")
    id_token: Optional[str] = None


class RefreshIn(BaseModel):
    refresh_token: str


class IntrospectOut(BaseModel):
    active: bool
    sub: Optional[StrUUID] = None
    tid: Optional[StrUUID] = None
    kind: Optional[str] = None


class PasswordGrantForm(BaseModel):
    grant_type: Literal["password"]
    username: str
    password: str


class AuthorizationCodeGrantForm(BaseModel):
    grant_type: Literal["authorization_code"]
    code: str
    redirect_uri: str
    client_id: str
    code_verifier: Optional[str] = None


class TokenRecord(RestOltpTable, GUIDPk, Timestamped):
    __tablename__ = "token_records"
    __table_args__ = ({"schema": "authn"},)

    token_hash: Mapped[str] = acol(
        storage=S(
            String(128),
            nullable=False,
            unique=True,
            index=True,
            default=lambda: uuid.uuid4().hex,
        )
    )
    jti: Mapped[str | None] = acol(
        storage=S(String(128), nullable=True, unique=True, index=True)
    )
    token_kind: Mapped[str] = acol(
        storage=S(String(32), nullable=False, default="access")
    )
    token_profile: Mapped[str | None] = acol(
        storage=S(String(128), nullable=True, index=True)
    )
    audience_digest: Mapped[str | None] = acol(
        storage=S(String(128), nullable=True, index=True)
    )
    sender_constraint_kind: Mapped[str | None] = acol(
        storage=S(String(64), nullable=True, index=True)
    )
    credential_or_grant_reference: Mapped[str | None] = acol(
        storage=S(String(255), nullable=True, index=True)
    )
    token_type_hint: Mapped[str | None] = acol(storage=S(String(64), nullable=True))
    token_status: Mapped[str] = acol(
        storage=S(String(32), nullable=False, default="active", index=True)
    )
    refresh_family_id: Mapped[str | None] = acol(
        storage=S(String(64), nullable=True, index=True)
    )
    refresh_parent_hash: Mapped[str | None] = acol(
        storage=S(String(128), nullable=True, index=True)
    )
    refresh_successor_hash: Mapped[str | None] = acol(
        storage=S(String(128), nullable=True, index=True)
    )
    active: Mapped[bool] = acol(storage=S(Boolean, nullable=False, default=True))
    subject: Mapped[str] = acol(
        storage=S(
            String(255),
            nullable=False,
            index=True,
            default="admin-created-token-record",
        )
    )
    tenant_id: Mapped[uuid.UUID | None] = acol(
        storage=S(
            PgUUID(as_uuid=True),
            fk=ForeignKeySpec(target="authn.tenants.id"),
            nullable=True,
            index=True,
        )
    )
    client_id: Mapped[uuid.UUID | None] = acol(
        storage=S(
            PgUUID(as_uuid=True),
            fk=ForeignKeySpec(target="authn.clients.id"),
            nullable=True,
            index=True,
        )
    )
    scope: Mapped[str | None] = acol(storage=S(String(1000), nullable=True))
    issuer: Mapped[str | None] = acol(storage=S(String(255), nullable=True))
    kid: Mapped[str | None] = acol(storage=S(String(255), nullable=True, index=True))
    key_version: Mapped[int | None] = acol(storage=S(Integer, nullable=True))
    audience: Mapped[dict | list | str | None] = acol(storage=S(JSON, nullable=True))
    claims: Mapped[dict | None] = acol(storage=S(JSON, nullable=True))
    issued_at: Mapped[dt.datetime] = acol(
        storage=S(
            TZDateTime, nullable=False, default=lambda: dt.datetime.now(dt.timezone.utc)
        )
    )
    expires_at: Mapped[dt.datetime | None] = acol(
        storage=S(TZDateTime, nullable=True, index=True)
    )
    last_introspected_at: Mapped[dt.datetime | None] = acol(
        storage=S(TZDateTime, nullable=True)
    )
    used_at: Mapped[dt.datetime | None] = acol(
        storage=S(TZDateTime, nullable=True, index=True)
    )
    reuse_detected_at: Mapped[dt.datetime | None] = acol(
        storage=S(TZDateTime, nullable=True, index=True)
    )
    revoked_at: Mapped[dt.datetime | None] = acol(
        storage=S(TZDateTime, nullable=True, index=True)
    )
    revoked_reason: Mapped[str | None] = acol(storage=S(String(128), nullable=True))


__all__ = [
    "AuthorizationCodeGrantForm",
    "IntrospectOut",
    "PasswordGrantForm",
    "RefreshIn",
    "TokenPair",
    "TokenRecord",
]

