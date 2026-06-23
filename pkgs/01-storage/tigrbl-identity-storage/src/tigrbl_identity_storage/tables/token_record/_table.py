"""Durable token status and introspection backing store."""

from __future__ import annotations

import datetime as dt
from pathlib import Path
import uuid
from typing import Any, Literal, Optional

from tigrbl.security import Depends as TigrblDepends
from tigrbl_identity_storage.framework import (
    AsyncSession,
    RestOltpTable,
    BaseModel,
    Field,
    Request,
    Timestamped,
    TigrblRouter,
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
from .._ops import create_record, field, first_record, list_records, record_id, update_record, utc_now
from ..engine import get_db


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


def _to_uuid(value: Any) -> uuid.UUID | None:
    if value is None or value == "" or value is False:
        return None
    if isinstance(value, uuid.UUID):
        return value
    try:
        return uuid.UUID(str(value))
    except Exception:
        return None


def _to_datetime(value: Any) -> dt.datetime | None:
    if value is None:
        return None
    if isinstance(value, dt.datetime):
        return value if value.tzinfo is not None else value.replace(tzinfo=dt.timezone.utc)
    try:
        return dt.datetime.fromtimestamp(int(value), tz=dt.timezone.utc)
    except Exception:
        return None


class TokenRecord(RestOltpTable, GUIDPk, Timestamped):
    __tablename__ = "token_records"
    __table_args__ = ({"schema": "authn"},)

    token_hash: Mapped[str] = acol(storage=S(String(128), nullable=False, unique=True, index=True, default=lambda: uuid.uuid4().hex))
    jti: Mapped[str | None] = acol(storage=S(String(128), nullable=True, unique=True, index=True))
    token_kind: Mapped[str] = acol(storage=S(String(32), nullable=False, default="access"))
    token_type_hint: Mapped[str | None] = acol(storage=S(String(64), nullable=True))
    token_status: Mapped[str] = acol(storage=S(String(32), nullable=False, default="active", index=True))
    refresh_family_id: Mapped[str | None] = acol(storage=S(String(64), nullable=True, index=True))
    refresh_parent_hash: Mapped[str | None] = acol(storage=S(String(128), nullable=True, index=True))
    refresh_successor_hash: Mapped[str | None] = acol(storage=S(String(128), nullable=True, index=True))
    active: Mapped[bool] = acol(storage=S(Boolean, nullable=False, default=True))
    subject: Mapped[str] = acol(storage=S(String(255), nullable=False, index=True, default="admin-created-token-record"))
    tenant_id: Mapped[uuid.UUID | None] = acol(
        storage=S(PgUUID(as_uuid=True), fk=ForeignKeySpec(target="authn.tenants.id"), nullable=True, index=True)
    )
    client_id: Mapped[uuid.UUID | None] = acol(
        storage=S(PgUUID(as_uuid=True), fk=ForeignKeySpec(target="authn.clients.id"), nullable=True, index=True)
    )
    scope: Mapped[str | None] = acol(storage=S(String(1000), nullable=True))
    issuer: Mapped[str | None] = acol(storage=S(String(255), nullable=True))
    kid: Mapped[str | None] = acol(storage=S(String(255), nullable=True, index=True))
    key_version: Mapped[int | None] = acol(storage=S(Integer, nullable=True))
    audience: Mapped[dict | list | str | None] = acol(storage=S(JSON, nullable=True))
    claims: Mapped[dict | None] = acol(storage=S(JSON, nullable=True))
    issued_at: Mapped[dt.datetime] = acol(
        storage=S(TZDateTime, nullable=False, default=lambda: dt.datetime.now(dt.timezone.utc))
    )
    expires_at: Mapped[dt.datetime | None] = acol(storage=S(TZDateTime, nullable=True, index=True))
    last_introspected_at: Mapped[dt.datetime | None] = acol(storage=S(TZDateTime, nullable=True))
    used_at: Mapped[dt.datetime | None] = acol(storage=S(TZDateTime, nullable=True, index=True))
    reuse_detected_at: Mapped[dt.datetime | None] = acol(storage=S(TZDateTime, nullable=True, index=True))
    revoked_at: Mapped[dt.datetime | None] = acol(storage=S(TZDateTime, nullable=True, index=True))
    revoked_reason: Mapped[str | None] = acol(storage=S(String(128), nullable=True))

    @classmethod
    async def persist_issued_token(
        cls,
        db: Any,
        *,
        token_hash: str,
        claims: dict[str, Any] | None = None,
        token_kind: str = "access",
        token_type_hint: str | None = None,
        refresh_family_id: str | None = None,
        refresh_parent_hash: str | None = None,
        refresh_successor_hash: str | None = None,
        **overrides: Any,
    ) -> "TokenRecord":
        claims = dict(claims or {})
        existing = await first_record(cls, db, {"token_hash": token_hash})
        payload = {
            "token_hash": token_hash,
            "jti": claims.get("jti") or overrides.pop("jti", None) or field(existing, "jti"),
            "token_kind": token_kind,
            "token_type_hint": token_type_hint or field(existing, "token_type_hint") or token_kind,
            "token_status": overrides.pop("token_status", None) or "active",
            "refresh_family_id": refresh_family_id or field(existing, "refresh_family_id"),
            "refresh_parent_hash": refresh_parent_hash or field(existing, "refresh_parent_hash"),
            "refresh_successor_hash": refresh_successor_hash or field(existing, "refresh_successor_hash"),
            "active": True,
            "subject": str(claims.get("sub") or field(existing, "subject") or ""),
            "tenant_id": _to_uuid(claims.get("tid") or field(existing, "tenant_id")),
            "client_id": _to_uuid(claims.get("client_id") or claims.get("azp") or field(existing, "client_id")),
            "scope": claims.get("scope") or field(existing, "scope"),
            "issuer": claims.get("iss") or field(existing, "issuer"),
            "kid": claims.get("kid") or overrides.pop("kid", None) or field(existing, "kid"),
            "key_version": overrides.pop("key_version", None) or claims.get("key_version") or field(existing, "key_version"),
            "audience": claims.get("aud") or field(existing, "audience"),
            "claims": claims,
            "issued_at": _to_datetime(overrides.pop("issued_at", None) or claims.get("iat")) or field(existing, "issued_at") or utc_now(),
            "expires_at": _to_datetime(overrides.pop("expires_at", None) or claims.get("exp")) or field(existing, "expires_at"),
            "used_at": overrides.pop("used_at", None) or field(existing, "used_at"),
            "reuse_detected_at": overrides.pop("reuse_detected_at", None) or field(existing, "reuse_detected_at"),
            "revoked_at": None,
            "revoked_reason": None,
        }
        payload.update(overrides)
        if existing is None:
            return await create_record(cls, db, payload)
        return await update_record(cls, db, record_id(existing), payload)

    @classmethod
    async def list_active_for_subject(
        cls,
        db: Any,
        *,
        subject: str,
        tenant_id: uuid.UUID | None = None,
        token_kind: str | None = None,
    ) -> list["TokenRecord"]:
        filters: dict[str, Any] = {"subject": subject}
        if tenant_id is not None:
            filters["tenant_id"] = tenant_id
        if token_kind is not None:
            filters["token_kind"] = token_kind
        now = utc_now()
        return [
            row
            for row in await list_records(cls, db, filters)
            if field(row, "active", True)
            and field(row, "token_status", "active") == "active"
            and field(row, "revoked_at") is None
            and (field(row, "expires_at") is None or field(row, "expires_at") > now)
        ]

    @classmethod
    async def revoke_family(
        cls,
        db: Any,
        *,
        refresh_family_id: str,
        reason: str = "refresh_token_reuse_detected",
        reuse_token_hash: str | None = None,
    ) -> list["TokenRecord"]:
        revoked = []
        now = utc_now()
        for row in await list_records(cls, db, {"refresh_family_id": refresh_family_id}):
            payload = {
                "active": False,
                "token_status": "revoked",
                "revoked_at": field(row, "revoked_at") or now,
                "revoked_reason": reason,
            }
            if reuse_token_hash and field(row, "token_hash") == reuse_token_hash:
                payload["reuse_detected_at"] = now
            revoked.append(await update_record(cls, db, record_id(row), payload))
        return revoked

    @classmethod
    async def mark_rotated(
        cls,
        db: Any,
        *,
        token_hash: str,
        successor_hash: str | None = None,
        reason: str = "refresh_rotated",
    ) -> "TokenRecord | None":
        row = await first_record(cls, db, {"token_hash": token_hash})
        if row is None:
            return None
        payload = {
            "used_at": utc_now(),
            "active": False,
            "token_status": "rotated",
            "revoked_at": utc_now(),
            "revoked_reason": reason,
        }
        if successor_hash:
            payload["refresh_successor_hash"] = successor_hash
        return await update_record(cls, db, record_id(row), payload)


api = router = TigrblRouter()


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[5]


@api.route("/token", methods=["POST"], response_model=TokenPair)
async def token(request: Request, db: AsyncSession = TigrblDepends(get_db)) -> Any:
    from ._route import token_request

    result = await token_request(request=request, db=db)
    from tigrbl_identity_storage.session_service import observe_token_response

    payload = result if isinstance(result, dict) else getattr(result, "model_dump", lambda **_: {})(mode="json")
    observe_token_response(
        _repo_root(),
        access_token=payload.get("access_token"),
        refresh_token=payload.get("refresh_token"),
        id_token=payload.get("id_token"),
        details=payload,
    )
    return result


TokenRecord.token = staticmethod(token)  # type: ignore[attr-defined]


__all__ = [
    "AuthorizationCodeGrantForm",
    "IntrospectOut",
    "PasswordGrantForm",
    "RefreshIn",
    "TokenPair",
    "TokenRecord",
    "api",
    "router",
    "token",
]
