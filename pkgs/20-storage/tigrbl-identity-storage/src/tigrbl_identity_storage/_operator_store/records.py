from __future__ import annotations

from .paths import *
from .paths import (
    _OPERATOR_DB_FILENAME,
    _append_jsonl_file,
    _metadata_payload,
    _write_metadata_snapshot,
)
from .app import operator_store_session
from tigrbl_identity_storage.tables._sync import run_async
from tigrbl_identity_storage.tables.operator_activity import OperatorActivity
from tigrbl_identity_storage.tables.operator_audit_event import OperatorAuditEvent
from tigrbl_identity_storage.tables.operator_metadata import OperatorMetadata
from tigrbl_identity_storage.tables.operator_record import OperatorRecord
from tigrbl_identity_storage.tables.operator_transaction import OperatorTransaction

def _load_records_from_snapshot(path: Path, *, tenant: str | None = None) -> dict[str, dict[str, Any]]:
    loaded = load_structured(path, default={})
    rows: dict[str, dict[str, Any]] = {}
    if isinstance(loaded, Mapping):
        items = loaded.values()
    elif isinstance(loaded, list):
        items = loaded
    else:
        items = []
    for item in items:
        if not isinstance(item, Mapping):
            continue
        record_id = item.get("id")
        if not record_id:
            continue
        if tenant is not None and item.get("tenant") != tenant:
            continue
        rows[str(record_id)] = copy.deepcopy(dict(item))
    return rows


async def _load_records_async(repo_root: Path, resource: str, tenant: str | None = None) -> dict[str, dict[str, Any]]:
    state_root = operator_state_root(repo_root)
    db_path = operator_database_path(repo_root)
    had_db = db_path.exists()
    async with operator_store_session(state_root) as db:
        rows = await OperatorRecord.load_records(db, resource, tenant=tenant)
    if rows or had_db or db_path.exists():
        return rows
    return _load_records_from_snapshot(resource_state_path(repo_root, resource), tenant=tenant)


def load_records(repo_root: Path, resource: str, tenant: str | None = None) -> dict[str, dict[str, Any]]:
    return run_async(_load_records_async(repo_root, resource, tenant=tenant))


def default_status(resource: str) -> str:
    if resource in {"keys"}:
        return "staged"
    return "active"


def deep_merge(base: Mapping[str, Any], patch: Mapping[str, Any]) -> dict[str, Any]:
    merged = copy.deepcopy(dict(base))
    for key, value in patch.items():
        if isinstance(value, Mapping) and isinstance(merged.get(key), Mapping):
            merged[key] = deep_merge(merged[key], value)
        else:
            merged[key] = copy.deepcopy(value)
    return merged


def make_record(resource: str, record_id: str, context: OperationContext, patch: Mapping[str, Any] | None = None) -> dict[str, Any]:
    patch = dict(patch or {})
    now = utc_now()
    data = copy.deepcopy(dict(patch))
    if context.tenant is None and data.get("tenant") is not None:
        tenant = str(data.pop("tenant"))
    else:
        tenant = context.tenant
    status = str(data.pop("status", default_status(resource)))
    enabled = bool(data.pop("enabled", status not in {"disabled", "revoked", "retired", "locked"}))
    return {
        "id": str(record_id),
        "resource": resource,
        "status": status,
        "enabled": enabled,
        "created_at": now,
        "updated_at": now,
        "actor": context.actor,
        "profile": context.profile,
        "tenant": tenant,
        "issuer": context.issuer,
        "revision": 1,
        "data": data,
    }


def matches_record(record: Mapping[str, Any], spec: FilterSpec) -> bool:
    if spec.status_filter and str(record.get("status")) != str(spec.status_filter):
        return False
    if spec.filter_expr:
        term = str(spec.filter_expr).strip().lower()
        haystacks = [
            str(record.get("id", "")).lower(),
            str(record.get("status", "")).lower(),
            str(record.get("tenant", "")).lower(),
            json.dumps(record.get("data", {}), sort_keys=True).lower(),
        ]
        data = record.get("data") or {}
        if isinstance(data, Mapping):
            for key in ("name", "display_name", "tenant_id", "client_id", "username", "email", "kid", "software_id"):
                haystacks.append(str(data.get(key, "")).lower())
        if not any(term in item for item in haystacks):
            return False
    return True


def sort_records(records: list[dict[str, Any]], sort_key: str = "id") -> list[dict[str, Any]]:
    def _sort_value(item: Mapping[str, Any]) -> tuple[str, str]:
        data = item.get("data") if isinstance(item.get("data"), Mapping) else {}
        primary = data.get(sort_key, item.get(sort_key, ""))
        return (str(primary or ""), str(item.get("id", "")))
    return [copy.deepcopy(dict(item)) for item in sorted(records, key=_sort_value)]


def list_records(repo_root: Path, resource: str, spec: FilterSpec | None = None, tenant: str | None = None) -> list[dict[str, Any]]:
    spec = spec or FilterSpec()
    records = load_records(repo_root, resource, tenant=tenant).values()
    filtered = [copy.deepcopy(dict(item)) for item in records if matches_record(item, spec)]
    sorted_items = sort_records(filtered, spec.sort)
    return sorted_items[spec.offset : spec.offset + spec.limit]


def latest_event(repo_root: Path, *, predicate=None) -> dict[str, Any] | None:
    items = sorted(read_jsonl(audit_log_path(repo_root)), key=lambda item: str(item.get("occurred_at", "")), reverse=True)
    if predicate is None:
        return items[0] if items else None
    for item in items:
        try:
            if predicate(item):
                return item
        except Exception:
            continue
    return None


def build_transaction_entry(
    context: OperationContext,
    *,
    status: str,
    record_id: str | None = None,
    changed_ids: list[str] | None = None,
    summary: Mapping[str, Any] | None = None,
    before_checksum: str | None = None,
    after_checksum: str | None = None,
) -> dict[str, Any]:
    return {
        "transaction_id": synthetic_id("txn"),
        "ts": utc_now(),
        "command": context.command,
        "resource": context.resource,
        "status": status,
        "record_id": record_id,
        "changed_ids": list(changed_ids or ([] if record_id is None else [record_id])),
        "summary": dict(summary or {}),
        "actor": context.actor,
        "profile": context.profile,
        "tenant": context.tenant,
        "issuer": context.issuer,
        "before_checksum": before_checksum,
        "after_checksum": after_checksum,
    }


def build_audit_entry(
    context: OperationContext,
    *,
    transaction_id: str,
    status: str,
    target_id: str | None = None,
    details: Mapping[str, Any] | None = None,
    source_surface: str = "operator",
) -> dict[str, Any]:
    return {
        "id": synthetic_id("audit"),
        "tenant_id": context.tenant,
        "actor_user_id": context.actor,
        "actor_client_id": None,
        "session_id": None,
        "event_type": context.command,
        "target_type": context.resource,
        "target_id": target_id,
        "outcome": status,
        "request_id": transaction_id,
        "occurred_at": utc_now(),
        "details": {**dict(details or {}), "source_surface": source_surface},
    }


def _sync_resource_snapshot(repo_root: Path, resource: str) -> None:
    rows = load_records(repo_root, resource, tenant=None)
    write_structured(resource_state_path(repo_root, resource), rows, fmt="json")
    _write_metadata_snapshot(repo_root)


async def _commit_mutation_async(
    context: OperationContext,
    *,
    records: Mapping[str, Mapping[str, Any]],
    transaction: Mapping[str, Any],
    audit_entry: Mapping[str, Any] | None = None,
) -> None:
    root = operator_state_root(context.repo_root)
    changed_ids = {str(item) for item in list(transaction.get("changed_ids") or [])}
    async with operator_store_session(root) as db:
        await OperatorRecord.replace_resource_records(
            db,
            resource=context.resource,
            records=records,
            tenant=context.tenant,
            actor=context.actor,
            changed_ids=changed_ids,
            dry_run=context.dry_run,
            now=utc_now(),
        )
        await OperatorTransaction.record_transaction(db, transaction)
        if audit_entry is not None:
            await OperatorAuditEvent.record_operator_audit(db, audit_entry)
        await OperatorActivity.record_activity(
            db,
            {
                "ts": utc_now(),
                "kind": context.command,
                "resource": context.resource,
                "id": transaction.get("record_id"),
                "status": transaction.get("status"),
                "transaction_id": transaction.get("transaction_id"),
            },
        )
        await OperatorMetadata.upsert_metadata(db, "last_transaction_id", transaction.get("transaction_id"))
        await OperatorMetadata.upsert_metadata(db, "last_transaction_status", transaction.get("status"))
        await OperatorMetadata.upsert_metadata(db, "repo_mutation_dependency", False)


def commit_mutation(context: OperationContext, *, records: Mapping[str, Mapping[str, Any]], transaction: Mapping[str, Any], audit_entry: Mapping[str, Any] | None = None) -> None:
    run_async(_commit_mutation_async(context, records=records, transaction=transaction, audit_entry=audit_entry))
    if not context.dry_run:
        _sync_resource_snapshot(context.repo_root, context.resource)
    _append_jsonl_file(transaction_log_path(context.repo_root), transaction)
    if audit_entry is not None:
        _append_jsonl_file(audit_log_path(context.repo_root), audit_entry)
    _append_jsonl_file(
        activity_log_path(context.repo_root),
        {
            "ts": utc_now(),
            "kind": context.command,
            "resource": context.resource,
            "id": transaction.get("record_id"),
            "status": transaction.get("status"),
            "transaction_id": transaction.get("transaction_id"),
        },
    )
    _write_metadata_snapshot(context.repo_root)


def _operator_root_from_path(path: Path) -> Path | None:
    if path.parent.name == "logs":
        return path.parent.parent
    if path.parent.name == "snapshots":
        return path.parent.parent
    return None


def _operator_table_for_log(path: Path) -> str | None:
    return {
        "transactions.jsonl": "transaction_log",
        "audit-events.jsonl": "audit_log",
        "activity.jsonl": "activity_log",
    }.get(path.name)


async def _read_operator_log_async(root: Path, table: str) -> list[dict[str, Any]]:
    async with operator_store_session(root) as db:
        if table == "transaction_log":
            return await OperatorTransaction.list_transactions(db)
        if table == "audit_log":
            return await OperatorAuditEvent.list_operator_audit(db)
        return await OperatorActivity.list_activity(db)


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    root = _operator_root_from_path(path)
    table = _operator_table_for_log(path)
    if root is not None and table is not None and (root / _OPERATOR_DB_FILENAME).exists():
        return run_async(_read_operator_log_async(root, table))
    return _jsonl_rows(path)


async def _append_operator_log_async(root: Path, table: str, payload: Mapping[str, Any]) -> None:
    async with operator_store_session(root) as db:
        if table == "transaction_log":
            await OperatorTransaction.record_transaction(db, payload)
        elif table == "audit_log":
            await OperatorAuditEvent.record_operator_audit(db, payload)
        else:
            await OperatorActivity.record_activity(db, payload)


def append_jsonl(path: Path, payload: Mapping[str, Any]) -> None:
    root = _operator_root_from_path(path)
    table = _operator_table_for_log(path)
    if root is not None and table is not None:
        run_async(_append_operator_log_async(root, table, payload))
        _append_jsonl_file(path, payload)
        return
    _append_jsonl_file(path, payload)


async def _ensure_operator_metadata_async(repo_root: Path) -> None:
    root = operator_state_root(repo_root)
    async with operator_store_session(root) as db:
        for key, value in _metadata_payload(repo_root).items():
            await OperatorMetadata.upsert_metadata(db, key, value)


def operator_store_summary(repo_root: Path) -> dict[str, Any]:
    run_async(_ensure_operator_metadata_async(repo_root))
    _write_metadata_snapshot(repo_root)
    payload = _metadata_payload(repo_root)
    payload.update(
        {
            "database_present": operator_database_path(repo_root).exists(),
            "audit_log_path": safe_display_path(audit_log_path(repo_root), repo_root, external_label="<operator-state>"),
            "transaction_log_path": safe_display_path(transaction_log_path(repo_root), repo_root, external_label="<operator-state>"),
            "activity_log_path": safe_display_path(activity_log_path(repo_root), repo_root, external_label="<operator-state>"),
        }
    )
    return payload


__all__ = [
    "ArtifactResult",
    "FilterSpec",
    "OPERATOR_STORE_SCHEMA_VERSION",
    "PORTABILITY_SCHEMA_VERSION",
    "OperationContext",
    "TransactionResult",
    "activity_log_path",
    "append_jsonl",
    "audit_log_path",
    "build_audit_entry",
    "build_transaction_entry",
    "commit_mutation",
    "deep_merge",
    "default_status",
    "display_path",
    "latest_event",
    "list_records",
    "load_records",
    "load_structured",
    "make_record",
    "matches_record",
    "operator_database_path",
    "operator_state_metadata_path",
    "operator_state_root",
    "operator_store_summary",
    "read_jsonl",
    "resource_state_path",
    "sha256_json",
    "sha256_path",
    "sort_records",
    "synthetic_id",
    "transaction_log_path",
    "utc_now",
    "validate_checksum",
    "write_structured",
]
