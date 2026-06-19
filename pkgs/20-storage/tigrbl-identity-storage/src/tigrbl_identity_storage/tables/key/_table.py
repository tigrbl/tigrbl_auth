"""Durable signing/encryption key metadata."""

from __future__ import annotations

import uuid
from typing import Any

from tigrbl_identity_storage.framework import (
    Base,
    GUIDPk,
    JSON,
    Integer,
    Mapped,
    PgUUID,
    S,
    String,
    Timestamped,
    acol,
    ForeignKeySpec,
)

from .._ops import create_record, field, first_record, list_records, read_record, record_id, update_record, utc_now


class Key(Base, GUIDPk, Timestamped):
    __tablename__ = "identity_keys"
    __table_args__ = ({"schema": "authn"},)

    kid: Mapped[str] = acol(storage=S(String(255), nullable=False, unique=True, index=True))
    algorithm: Mapped[str] = acol(storage=S(String(64), nullable=False, index=True))
    key_use: Mapped[str] = acol(storage=S(String(32), nullable=False, default="sig"))
    status: Mapped[str] = acol(storage=S(String(32), nullable=False, default="active", index=True))
    primary_version: Mapped[int | None] = acol(storage=S(Integer, nullable=True, default=1))
    provider: Mapped[str | None] = acol(storage=S(String(255), nullable=True))
    provider_key_ref: Mapped[str | None] = acol(storage=S(String(1000), nullable=True))
    public_jwk: Mapped[dict | None] = acol(storage=S(JSON, nullable=True))
    key_metadata: Mapped[dict | None] = acol(storage=S(JSON, nullable=True))
    tenant_id: Mapped[uuid.UUID | None] = acol(
        storage=S(PgUUID(as_uuid=True), fk=ForeignKeySpec(target="authn.tenants.id"), nullable=True, index=True)
    )
    realm_id: Mapped[uuid.UUID | None] = acol(
        storage=S(PgUUID(as_uuid=True), fk=ForeignKeySpec(target="authn.realms.id"), nullable=True, index=True)
    )

    @classmethod
    async def create_key(
        cls,
        db: Any,
        *,
        kid: str,
        algorithm: str,
        key_use: str = "sig",
        status: str = "active",
        primary_version: int | None = 1,
        provider: str | None = None,
        provider_key_ref: str | None = None,
        public_jwk: dict | None = None,
        key_metadata: dict | None = None,
        tenant_id: uuid.UUID | None = None,
        realm_id: uuid.UUID | None = None,
    ) -> "Key":
        return await create_record(
            cls,
            db,
            {
                "kid": kid,
                "algorithm": algorithm,
                "key_use": key_use,
                "status": status,
                "primary_version": primary_version,
                "provider": provider,
                "provider_key_ref": provider_key_ref,
                "public_jwk": public_jwk,
                "key_metadata": key_metadata,
                "tenant_id": tenant_id,
                "realm_id": realm_id,
            },
        )

    @classmethod
    async def lookup_by_kid(cls, db: Any, *, kid: str, tenant_id: uuid.UUID | None = None) -> "Key | None":
        filters: dict[str, Any] = {"kid": kid}
        if tenant_id is not None:
            filters["tenant_id"] = tenant_id
        return await first_record(cls, db, filters)

    @classmethod
    async def list_active(cls, db: Any, *, tenant_id: uuid.UUID | None = None, key_use: str | None = None) -> list["Key"]:
        filters: dict[str, Any] = {"status": "active"}
        if tenant_id is not None:
            filters["tenant_id"] = tenant_id
        if key_use is not None:
            filters["key_use"] = key_use
        return await list_records(cls, db, filters)

    @classmethod
    async def enable(cls, db: Any, *, id: Any) -> "Key":
        return await update_record(cls, db, id, {"status": "active"})

    @classmethod
    async def disable(cls, db: Any, *, id: Any) -> "Key":
        return await update_record(cls, db, id, {"status": "disabled"})

    @classmethod
    async def retire(cls, db: Any, *, id: Any) -> "Key":
        return await update_record(cls, db, id, {"status": "retired", "key_metadata": {"retired_at": utc_now().isoformat()}})

    @classmethod
    async def rotate(
        cls,
        db: Any,
        *,
        id: Any | None = None,
        kid: str | None = None,
        public_jwk: dict | None = None,
        provider_key_ref: str | None = None,
        provider: str | None = None,
        actor_user_id: uuid.UUID | None = None,
        actor_client_id: uuid.UUID | None = None,
        details: dict | None = None,
    ) -> "Key":
        from ..key_rotation_event import KeyRotationEvent
        from ..key_version import KeyVersion

        row = await read_record(cls, db, id) if id is not None else None
        if row is None and kid is not None:
            row = await cls.lookup_by_kid(db, kid=kid)
        if row is None:
            raise LookupError("key not found")

        next_version = int(field(row, "primary_version", 0) or 0) + 1
        await KeyVersion.create_version(
            db,
            key_id=record_id(row),
            version=next_version,
            status="active",
            public_jwk=public_jwk,
            provider_key_ref=provider_key_ref,
            provider=provider or field(row, "provider"),
        )
        updated = await update_record(
            cls,
            db,
            record_id(row),
            {
                "primary_version": next_version,
                "public_jwk": public_jwk or field(row, "public_jwk"),
                "provider_key_ref": provider_key_ref or field(row, "provider_key_ref"),
                "provider": provider or field(row, "provider"),
            },
        )
        await KeyRotationEvent.record_rotation(
            db,
            key_kid=field(row, "kid"),
            algorithm=field(row, "algorithm"),
            tenant_id=field(row, "tenant_id"),
            actor_user_id=actor_user_id,
            actor_client_id=actor_client_id,
            details={"version": next_version, **(details or {})},
        )
        return updated

    @classmethod
    async def publish_jwks(cls, db: Any, *, tenant_id: uuid.UUID | None = None) -> dict[str, list[dict[str, Any]]]:
        keys = []
        for row in await cls.list_active(db, tenant_id=tenant_id):
            jwk = field(row, "public_jwk")
            if isinstance(jwk, dict):
                keys.append({key: value for key, value in jwk.items() if key not in {"d", "p", "q", "dp", "dq", "qi"}})
        return {"keys": keys}

    @classmethod
    async def sign(cls, db: Any, *, kid: str, payload: bytes | str, ctx: dict[str, Any] | None = None) -> Any:
        row = await cls.lookup_by_kid(db, kid=kid)
        if row is None or field(row, "status") != "active":
            raise LookupError("active key not found")
        signer = (ctx or {}).get("signer")
        if signer is None:
            raise LookupError("signer provider not available")
        request = (ctx or {}).get("sign_request_factory")
        if callable(request):
            return await signer.sign(request(row=row, payload=payload))
        return await signer.sign(payload, key_ref=field(row, "provider_key_ref"), kid=kid)

    @classmethod
    async def verify(
        cls,
        db: Any,
        *,
        kid: str,
        payload: bytes | str,
        signature: bytes | str,
        ctx: dict[str, Any] | None = None,
    ) -> Any:
        row = await cls.lookup_by_kid(db, kid=kid)
        if row is None:
            raise LookupError("key not found")
        verifier = (ctx or {}).get("verifier") or (ctx or {}).get("signer")
        if verifier is None:
            raise LookupError("verifier provider not available")
        request = (ctx or {}).get("verify_request_factory")
        if callable(request):
            return await verifier.verify(request(row=row, payload=payload, signature=signature))
        return await verifier.verify(payload, signature=signature, public_jwk=field(row, "public_jwk"), kid=kid)


__all__ = ["Key"]
