"""Shared helpers for implementation-backed RPC methods."""

from __future__ import annotations

import csv
import io
import json
from datetime import date, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence
from uuid import UUID

from tigrbl_auth.api.rpc.registry import RpcRequestContext


def repo_root_from_context(context: RpcRequestContext) -> Path:
    return context.resolved_repo_root()


def maybe_uuid(value: Any) -> Any:
    if value in {None, "", False}:
        return None
    if isinstance(value, UUID):
        return value
    try:
        return UUID(str(value))
    except Exception:
        return value


def to_wire(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {str(key): to_wire(item) for key, item in value.items()}
    if isinstance(value, (list, tuple, set)):
        return [to_wire(item) for item in value]
    if isinstance(value, (datetime, date)):
        return value.isoformat()
    if isinstance(value, UUID):
        return str(value)
    if isinstance(value, bytes):
        return value.hex()
    if isinstance(value, Path):
        return str(value)
    return value


def row_to_dict(row: Any, *, extra_metadata: dict[str, Any] | None = None) -> dict[str, Any]:
    data: dict[str, Any] = {}
    table = getattr(row, "__table__", None)
    if table is not None:
        for column in table.columns:
            data[column.name] = to_wire(getattr(row, column.name))
    elif hasattr(row, "model_dump"):
        data = to_wire(row.model_dump(mode="json"))
    elif isinstance(row, Mapping):
        data = to_wire(dict(row))
    else:
        data = {"value": to_wire(row)}
    if extra_metadata:
        data.setdefault("metadata", {}).update(extra_metadata)
    return data


def read_yaml(path: Path) -> Any:
    import yaml

    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def export_records(records: Sequence[Mapping[str, Any]], export_format: str) -> str:
    export_format = str(export_format).lower()
    if export_format in {"json", "application/json"}:
        return json.dumps([to_wire(item) for item in records], indent=2, sort_keys=True)
    if export_format in {"ndjson", "jsonl"}:
        return "\n".join(json.dumps(to_wire(item), sort_keys=True) for item in records)
    if export_format == "csv":
        rows = [to_wire(item) for item in records]
        keys: list[str] = []
        for row in rows:
            for key in row.keys():
                if key not in keys:
                    keys.append(str(key))
        buf = io.StringIO()
        writer = csv.DictWriter(buf, fieldnames=keys)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key) for key in keys})
        return buf.getvalue()
    raise ValueError(f"unsupported export format: {export_format}")


def _db_handles():
    try:
        from tigrbl_auth.services.persistence import _session
    except Exception as exc:  # pragma: no cover - surfaced when runtime deps are absent
        raise RuntimeError("database-backed RPC methods require the runtime dependency set") from exc
    return _session


async def _ensure_schema_ready() -> None:
    from tigrbl_auth.migrations.runtime import apply_all_async

    await apply_all_async()


def _created_item(value: Any) -> Any:
    if isinstance(value, Mapping):
        for key in ("item", "result", "data"):
            if key in value:
                return value[key]
    return value


def _list_items(result: Any) -> list[Any]:
    if isinstance(result, Mapping) and isinstance(result.get("items"), list):
        result = result["items"]
    elif hasattr(result, "items"):
        result = result.items
    if isinstance(result, list):
        return result
    if isinstance(result, tuple):
        return list(result)
    if result is None:
        return []
    return [result]


def _value_matches(actual: Any, expected: Any) -> bool:
    if actual == expected:
        return True
    if actual is None or expected is None:
        return False
    return str(actual) == str(expected)


def _matches_filters(row: Any, filters: Mapping[str, Any]) -> bool:
    for key, expected in filters.items():
        if expected is None:
            continue
        if not hasattr(row, key):
            continue
        if not _value_matches(getattr(row, key, None), maybe_uuid(expected)):
            return False
    return True


async def list_rows(
    model: Any,
    *,
    filters: dict[str, Any] | None = None,
    limit: int = 50,
    offset: int = 0,
    order_by: str | None = "created_at",
    descending: bool = True,
) -> list[Any]:
    _session = _db_handles()
    await _ensure_schema_ready()
    async with _session() as session:
        normalized_filters = {
            key: maybe_uuid(value)
            for key, value in (filters or {}).items()
            if value is not None
        }
        result = await model.handlers.list.core({"payload": {"filters": normalized_filters}, "db": session})
        rows = [row for row in _list_items(result) if _matches_filters(row, normalized_filters)]
        if order_by:
            rows = sorted(
                rows,
                key=lambda row: getattr(row, order_by, None) or "",
                reverse=descending,
            )
        return rows[offset : offset + limit]


async def get_row(model: Any, *, id_value: Any | None = None, filters: dict[str, Any] | None = None) -> Any | None:
    _session = _db_handles()
    await _ensure_schema_ready()
    async with _session() as session:
        if id_value is not None and hasattr(model, "id"):
            row = await model.handlers.read.core({"path_params": {"id": maybe_uuid(id_value)}, "db": session})
            if row is not None and _matches_filters(row, filters or {}):
                return row
            return None
        rows = await list_rows(model, filters=filters, limit=1, offset=0, order_by=None)
        return rows[0] if rows else None


async def create_key_rotation_event(*, key_kid: str, action: str, status: str, details: dict[str, Any] | None = None) -> dict[str, Any]:
    _session = _db_handles()
    from tigrbl_auth.tables import KeyRotationEvent

    await _ensure_schema_ready()
    async with _session() as session:
        row = await KeyRotationEvent.handlers.create.core(
            {
                "payload": {
                    "key_kid": key_kid,
                    "action": action,
                    "status": status,
                    "details": details or {},
                },
                "db": session,
            }
        )
        row = _created_item(row)
        return row_to_dict(row)


def deployment_summary(deployment: Any) -> dict[str, Any]:
    return {
        "profile": str(getattr(deployment, "profile", "baseline")),
        "plugin_mode": str(getattr(deployment, "plugin_mode", "mixed")),
        "runtime_style": str(getattr(deployment, "runtime_style", "standalone")),
        "surface_sets": list(getattr(deployment, "surface_sets", ()) or ()),
        "protocol_slices": list(getattr(deployment, "protocol_slices", ()) or ()),
        "active_routes": list(getattr(deployment, "active_routes", ()) or ()),
        "active_targets": list(getattr(deployment, "active_targets", ()) or ()),
        "active_openrpc_methods": list(getattr(deployment, "active_openrpc_methods", ()) or ()),
    }
