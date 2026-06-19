"""Table-owned operator resource records."""

from __future__ import annotations

import copy
import json
from typing import Any, Mapping

from tigrbl_identity_storage.framework import Base, Boolean, Mapped, S, String, acol

from ._ops import create_record, delete_record, field, first_record, list_records, record_id, update_record


def _default_status(resource: str) -> str:
    return "staged" if resource in {"keys"} else "active"


class OperatorRecord(Base):
    __tablename__ = "operator_records"

    id: Mapped[str] = acol(storage=S(String(512), primary_key=True, nullable=False))
    resource: Mapped[str] = acol(storage=S(String(128), nullable=False, index=True))
    record_id: Mapped[str] = acol(storage=S(String(255), nullable=False, index=True))
    status: Mapped[str] = acol(storage=S(String(64), nullable=False, default="active", index=True))
    enabled: Mapped[bool] = acol(storage=S(Boolean, nullable=False, default=True))
    created_at: Mapped[str] = acol(storage=S(String(64), nullable=False))
    updated_at: Mapped[str] = acol(storage=S(String(64), nullable=False))
    actor: Mapped[str | None] = acol(storage=S(String(255), nullable=True))
    profile: Mapped[str | None] = acol(storage=S(String(255), nullable=True))
    tenant: Mapped[str | None] = acol(storage=S(String(255), nullable=True, index=True))
    issuer: Mapped[str | None] = acol(storage=S(String(512), nullable=True))
    revision: Mapped[int] = acol(storage=S(nullable=False, default=1))
    data_json: Mapped[str] = acol(storage=S(String(20000), nullable=False, default="{}"))

    @staticmethod
    def store_id(resource: str, record_id: str) -> str:
        return f"{resource}:{record_id}"

    @classmethod
    def row_to_record(cls, row: Any) -> dict[str, Any]:
        data = json.loads(field(row, "data_json") or "{}")
        if not isinstance(data, Mapping):
            data = {}
        return {
            "id": str(field(row, "record_id")),
            "resource": str(field(row, "resource")),
            "status": str(field(row, "status")),
            "enabled": bool(field(row, "enabled")),
            "created_at": str(field(row, "created_at")),
            "updated_at": str(field(row, "updated_at")),
            "actor": field(row, "actor"),
            "profile": field(row, "profile"),
            "tenant": field(row, "tenant"),
            "issuer": field(row, "issuer"),
            "revision": int(field(row, "revision") or 1),
            "data": copy.deepcopy(dict(data)),
        }

    @classmethod
    def normalize_record(
        cls,
        resource: str,
        rec_id: str,
        record: Mapping[str, Any],
        *,
        fallback_actor: str | None = None,
        fallback_now: str,
    ) -> dict[str, Any]:
        data = record.get("data") if isinstance(record.get("data"), Mapping) else {}
        status = str(record.get("status") or _default_status(resource))
        return {
            "id": str(rec_id),
            "resource": resource,
            "status": status,
            "enabled": bool(record.get("enabled", status not in {"disabled", "revoked", "retired", "locked"})),
            "created_at": str(record.get("created_at") or fallback_now),
            "updated_at": str(record.get("updated_at") or fallback_now),
            "actor": record.get("actor") or fallback_actor,
            "profile": record.get("profile"),
            "tenant": record.get("tenant"),
            "issuer": record.get("issuer"),
            "revision": int(record.get("revision") or 1),
            "data": copy.deepcopy(dict(data)),
        }

    @classmethod
    def payload_from_record(cls, record: Mapping[str, Any]) -> dict[str, Any]:
        return {
            "id": cls.store_id(str(record["resource"]), str(record["id"])),
            "resource": str(record["resource"]),
            "record_id": str(record["id"]),
            "status": str(record["status"]),
            "enabled": bool(record.get("enabled", True)),
            "created_at": str(record["created_at"]),
            "updated_at": str(record["updated_at"]),
            "actor": record.get("actor"),
            "profile": record.get("profile"),
            "tenant": record.get("tenant"),
            "issuer": record.get("issuer"),
            "revision": int(record.get("revision") or 1),
            "data_json": json.dumps(dict(record.get("data") or {}), sort_keys=True),
        }

    @classmethod
    async def load_records(cls, db: Any, resource: str, tenant: str | None = None) -> dict[str, dict[str, Any]]:
        filters: dict[str, Any] = {"resource": resource}
        if tenant is not None:
            filters["tenant"] = tenant
        rows = await list_records(cls, db, filters)
        return {str(field(row, "record_id")): cls.row_to_record(row) for row in rows}

    @classmethod
    async def replace_resource_records(
        cls,
        db: Any,
        *,
        resource: str,
        records: Mapping[str, Mapping[str, Any]],
        tenant: str | None,
        actor: str | None,
        changed_ids: set[str],
        dry_run: bool,
        now: str,
    ) -> dict[str, dict[str, Any]]:
        existing_rows = await list_records(cls, db, {"resource": resource})
        existing_all = {str(field(row, "record_id")): cls.row_to_record(row) for row in existing_rows}
        if tenant is None:
            full_records = {
                str(key): cls.normalize_record(resource, str(key), value, fallback_actor=actor, fallback_now=now)
                for key, value in records.items()
            }
        else:
            preserved = {rec_id: record for rec_id, record in existing_all.items() if record.get("tenant") != tenant}
            scoped = {
                str(key): cls.normalize_record(resource, str(key), value, fallback_actor=actor, fallback_now=now)
                for key, value in records.items()
            }
            for row in scoped.values():
                row["tenant"] = tenant
            full_records = {**preserved, **scoped}

        if not dry_run:
            for row in existing_rows:
                await delete_record(cls, db, record_id(row))
            for rec_id in sorted(full_records):
                record = copy.deepcopy(full_records[rec_id])
                previous = existing_all.get(rec_id)
                incoming_revision = int(record.get("revision") or 1)
                if previous is None:
                    record["revision"] = max(1, incoming_revision)
                elif rec_id in changed_ids and _without_revision(previous) != _without_revision(record):
                    record["revision"] = max(int(previous.get("revision") or 0) + 1, incoming_revision)
                else:
                    record["revision"] = max(int(previous.get("revision") or 1), incoming_revision)
                existing = await first_record(cls, db, {"id": cls.store_id(resource, rec_id)})
                payload = cls.payload_from_record(record)
                if existing is None:
                    await create_record(cls, db, payload)
                else:
                    await update_record(cls, db, record_id(existing), payload)
        return full_records


def _without_revision(record: Mapping[str, Any]) -> dict[str, Any]:
    cleaned = copy.deepcopy(dict(record))
    cleaned.pop("revision", None)
    return cleaned


__all__ = ["OperatorRecord"]
