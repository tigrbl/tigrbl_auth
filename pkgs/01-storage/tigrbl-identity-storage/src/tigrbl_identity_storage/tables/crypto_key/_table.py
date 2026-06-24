"""Durable provider-neutral crypto key metadata."""

from __future__ import annotations

import uuid
from typing import Any

from tigrbl_identity_storage.framework import (
    Boolean,
    ForeignKeySpec,
    GUIDPk,
    Integer,
    JSON,
    Mapped,
    PgUUID,
    RestOltpTable,
    S,
    String,
    Timestamped,
    acol,
)

from .._ops import create_record, field, first_record, list_records, read_record, record_id, update_record, utc_now
from ._usage import normalize_payload_key_usage, stored_key_operations, stored_key_usages


class CryptoKey(RestOltpTable, GUIDPk, Timestamped):
    __tablename__ = "crypto_keys"
    __table_args__ = ({"schema": "authn"},)

    kid: Mapped[str] = acol(storage=S(String(255), nullable=False, unique=True, index=True))
    algorithm: Mapped[str] = acol(storage=S(String(64), nullable=False, index=True))
    key_kind: Mapped[str] = acol(storage=S(String(64), nullable=False, default="asymmetric", index=True))
    key_usages: Mapped[list[str] | None] = acol(storage=S(JSON, nullable=True))
    allowed_ops: Mapped[list[str] | None] = acol(storage=S(JSON, nullable=True))
    status: Mapped[str] = acol(storage=S(String(32), nullable=False, default="active", index=True))
    primary_version: Mapped[int | None] = acol(storage=S(Integer, nullable=True, default=1))
    provider: Mapped[str | None] = acol(storage=S(String(255), nullable=True, index=True))
    provider_key_ref: Mapped[str | None] = acol(storage=S(String(1000), nullable=True))
    export_policy: Mapped[str] = acol(storage=S(String(64), nullable=False, default="public_only", index=True))
    origin: Mapped[str] = acol(storage=S(String(64), nullable=False, default="generated", index=True))
    extractable: Mapped[bool] = acol(storage=S(Boolean, nullable=False, default=False))
    public_material_format: Mapped[str | None] = acol(storage=S(String(64), nullable=True))
    public_material: Mapped[dict | str | None] = acol(storage=S(JSON, nullable=True))
    fingerprint: Mapped[str | None] = acol(storage=S(String(255), nullable=True, index=True))
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
        key_kind: str = "asymmetric",
        key_usages: Any = None,
        allowed_ops: Any = None,
        status: str = "active",
        primary_version: int | None = 1,
        provider: str | None = None,
        provider_key_ref: str | None = None,
        export_policy: str = "public_only",
        origin: str = "generated",
        extractable: bool = False,
        public_material_format: str | None = None,
        public_material: dict | str | None = None,
        fingerprint: str | None = None,
        key_metadata: dict | None = None,
        tenant_id: uuid.UUID | None = None,
        realm_id: uuid.UUID | None = None,
    ) -> "CryptoKey":
        usage_record = normalize_payload_key_usage(
            {
                "key_kind": key_kind,
                "key_usages": key_usages,
                "allowed_ops": allowed_ops,
            }
        )
        return await create_record(
            cls,
            db,
            {
                "kid": kid,
                "algorithm": algorithm,
                "key_kind": usage_record["key_kind"],
                "key_usages": usage_record["key_usages"],
                "allowed_ops": usage_record["allowed_ops"],
                "status": status,
                "primary_version": primary_version,
                "provider": provider,
                "provider_key_ref": provider_key_ref,
                "export_policy": export_policy,
                "origin": origin,
                "extractable": extractable,
                "public_material_format": public_material_format,
                "public_material": public_material,
                "fingerprint": fingerprint,
                "key_metadata": key_metadata,
                "tenant_id": tenant_id,
                "realm_id": realm_id,
            },
        )

    @classmethod
    async def lookup_by_kid(cls, db: Any, *, kid: str, tenant_id: uuid.UUID | None = None) -> "CryptoKey | None":
        filters: dict[str, Any] = {"kid": kid}
        if tenant_id is not None:
            filters["tenant_id"] = tenant_id
        return await first_record(cls, db, filters)

    @classmethod
    async def list_active(
        cls,
        db: Any,
        *,
        tenant_id: uuid.UUID | None = None,
        key_usage: str | None = None,
        operation: str | None = None,
    ) -> list["CryptoKey"]:
        filters: dict[str, Any] = {"status": "active"}
        if tenant_id is not None:
            filters["tenant_id"] = tenant_id
        rows = await list_records(cls, db, filters)
        if key_usage is not None:
            rows = [row for row in rows if key_usage in set(field(row, "key_usages", []) or [])]
        if operation is not None:
            rows = [row for row in rows if operation in set(field(row, "allowed_ops", []) or [])]
        return rows

    @classmethod
    async def retire(cls, db: Any, *, id: Any) -> "CryptoKey":
        row = await read_record(cls, db, id)
        metadata = dict(field(row, "key_metadata", {}) or {}) if row is not None else {}
        metadata["retired_at"] = utc_now().isoformat()
        return await update_record(cls, db, id, {"status": "retired", "key_metadata": metadata})

    @classmethod
    async def rotate_record(
        cls,
        db: Any,
        *,
        id: Any | None = None,
        kid: str | None = None,
        public_material: dict | str | None = None,
        public_material_format: str | None = None,
        provider_key_ref: str | None = None,
        provider: str | None = None,
        allowed_ops: Any = None,
        actor_user_id: uuid.UUID | None = None,
        actor_client_id: uuid.UUID | None = None,
        details: dict | None = None,
    ) -> "CryptoKey":
        from ..crypto_key_version import CryptoKeyVersion
        from ..key_rotation_event import KeyRotationEvent

        row = await read_record(cls, db, id) if id is not None else None
        if row is None and kid is not None:
            row = await cls.lookup_by_kid(db, kid=kid)
        if row is None:
            raise LookupError("crypto key not found")

        next_version = int(field(row, "primary_version", 0) or 0) + 1
        await CryptoKeyVersion.create_version(
            db,
            key_id=record_id(row),
            version=next_version,
            status="active",
            public_material=public_material,
            public_material_format=public_material_format or field(row, "public_material_format"),
            provider_key_ref=provider_key_ref,
            provider=provider or field(row, "provider"),
            allowed_ops=stored_key_operations(
                key_kind=field(row, "key_kind"),
                key_usages=field(row, "key_usages"),
                allowed_ops=allowed_ops if allowed_ops is not None else field(row, "allowed_ops"),
            ),
        )
        next_allowed_ops = stored_key_operations(
            key_kind=field(row, "key_kind"),
            key_usages=field(row, "key_usages"),
            allowed_ops=allowed_ops if allowed_ops is not None else field(row, "allowed_ops"),
        )
        updated = await update_record(
            cls,
            db,
            record_id(row),
            {
                "primary_version": next_version,
                "public_material": public_material or field(row, "public_material"),
                "public_material_format": public_material_format or field(row, "public_material_format"),
                "provider_key_ref": provider_key_ref or field(row, "provider_key_ref"),
                "provider": provider or field(row, "provider"),
                "key_usages": stored_key_usages(field(row, "key_usages")),
                "allowed_ops": next_allowed_ops,
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


__all__ = ["CryptoKey"]
