from __future__ import annotations

"""Production-grade durable operator service layer shared by CLI and RPC."""

import copy
import hashlib
import json
from pathlib import Path
from typing import Any, Mapping

from tigrbl_identity_storage_runtime.operator_store import (
    ArtifactResult,
    FilterSpec,
    OperationContext,
    TransactionResult,
    build_audit_entry,
    build_transaction_entry,
    commit_mutation,
    deep_merge,
    display_path,
    latest_event,
    list_records,
    load_records,
    make_record,
    operator_state_root,
    operator_store_summary,
    PORTABILITY_SCHEMA_VERSION,
    read_jsonl,
    resource_state_path,
    sha256_json,
    synthetic_id,
    utc_now,
    validate_checksum,
    write_structured,
    transaction_log_path,
    audit_log_path,
    activity_log_path,
)
GENERIC_RESOURCES = {"tenant", "client", "identity", "flow", "session", "token", "keys"}


class OperatorStateError(RuntimeError):
    def __init__(self, *, code: int, status: str, reason: str, payload: dict[str, Any] | None = None) -> None:
        super().__init__(reason)
        self.code = int(code)
        self.status = status
        self.reason = reason
        self.payload = payload or {}

    def to_payload(self, command: str, resource: str) -> dict[str, Any]:
        return {"command": command, "resource": resource, "status": self.status, "reason": self.reason, **self.payload}


def _filters(*, status_filter: str | None = None, filter_expr: str | None = None, sort: str = "id", offset: int = 0, limit: int = 50) -> FilterSpec:
    return FilterSpec(status_filter=status_filter, filter_expr=filter_expr, sort=sort, offset=offset, limit=limit)


def _list(repo_root: Path, resource: str, *, status_filter: str | None = None, filter_expr: str | None = None, sort: str = "id", offset: int = 0, limit: int = 50, tenant: str | None = None) -> list[dict[str, Any]]:
    return list_records(repo_root, resource, _filters(status_filter=status_filter, filter_expr=filter_expr, sort=sort, offset=offset, limit=limit), tenant=tenant)


def get_record(repo_root: Path, resource: str, record_id: str, *, tenant: str | None = None) -> dict[str, Any] | None:
    return copy.deepcopy(load_records(repo_root, resource, tenant=tenant).get(str(record_id)))


def list_resource(repo_root: Path, resource: str, *, status_filter: str | None = None, filter_expr: str | None = None, sort: str = "id", offset: int = 0, limit: int = 50, tenant: str | None = None) -> list[dict[str, Any]]:
    return _list(repo_root, resource, status_filter=status_filter, filter_expr=filter_expr, sort=sort, offset=offset, limit=limit, tenant=tenant)


def _commit_records(context: OperationContext, *, records: Mapping[str, Mapping[str, Any]], status: str, target_id: str | None, changed_ids: list[str] | None = None, summary: Mapping[str, Any] | None = None) -> str:
    before_checksum = sha256_json(load_records(context.repo_root, context.resource, tenant=context.tenant))
    after_checksum = sha256_json(records)
    transaction = build_transaction_entry(
        context,
        status=status,
        record_id=target_id,
        changed_ids=changed_ids,
        summary=summary,
        before_checksum=before_checksum,
        after_checksum=after_checksum,
    )
    audit_entry = build_audit_entry(context, transaction_id=str(transaction["transaction_id"]), status=status, target_id=target_id, details=summary)
    commit_mutation(context, records=records, transaction=transaction, audit_entry=audit_entry)
    return str(transaction["transaction_id"])


def _sanitize_patch_for_scope(context: OperationContext, patch: Mapping[str, Any] | None = None) -> dict[str, Any]:
    payload = dict(patch or {})
    if context.tenant is not None:
        patch_tenant = payload.get("tenant")
        if patch_tenant not in {None, context.tenant}:
            raise OperatorStateError(code=1, status="validation_error", reason=f"tenant mismatch for {context.resource}", payload={"tenant": patch_tenant, "expected_tenant": context.tenant})
        payload["tenant"] = context.tenant
    return payload


def _tenant_value(context: OperationContext, record: Mapping[str, Any]) -> str | None:
    if context.tenant is not None:
        return context.tenant
    tenant = record.get("tenant")
    return str(tenant) if tenant not in {None, ""} else None


def create_resource(context: OperationContext, *, record_id: str | None, patch: Mapping[str, Any] | None = None, if_exists: str = "error") -> TransactionResult:
    patch = _sanitize_patch_for_scope(context, patch)
    records = load_records(context.repo_root, context.resource, tenant=context.tenant)
    chosen_id = str(record_id or patch.get("id") or synthetic_id(context.resource))
    existing = records.get(chosen_id)
    if existing is not None:
        if if_exists == "skip":
            return TransactionResult(synthetic_id("txn"), context.command, context.resource, "skipped", context.dry_run, False, record=copy.deepcopy(existing), summary={"if_exists": if_exists})
        if if_exists == "error":
            raise OperatorStateError(code=2, status="conflict", reason=f"{context.resource} {chosen_id} already exists", payload={"id": chosen_id})
        if if_exists in {"update", "replace"}:
            record = copy.deepcopy(existing)
            if if_exists == "replace":
                record["data"] = dict(patch)
            else:
                record["data"] = deep_merge(record.get("data", {}), patch)
            if patch.get("tenant") is not None:
                record["tenant"] = str(patch["tenant"])
                record.setdefault("data", {}).pop("tenant", None)
            record["updated_at"] = utc_now()
            new_records = dict(records)
            new_records[chosen_id] = record
            transaction_id = _commit_records(context, records=new_records, status="updated", target_id=chosen_id, changed_ids=[chosen_id], summary={"mutation": "create", "if_exists": if_exists})
            return TransactionResult(transaction_id, context.command, context.resource, "updated", context.dry_run, not context.dry_run, record=record, changed_ids=[chosen_id], summary={"if_exists": if_exists})
        raise OperatorStateError(code=1, status="validation_error", reason=f"unsupported if_exists policy: {if_exists}")
    record = make_record(context.resource, chosen_id, context, patch)
    new_records = dict(records)
    new_records[chosen_id] = record
    transaction_id = _commit_records(context, records=new_records, status="created", target_id=chosen_id, changed_ids=[chosen_id], summary={"mutation": "create"})
    return TransactionResult(transaction_id, context.command, context.resource, "created", context.dry_run, not context.dry_run, record=record, changed_ids=[chosen_id])


def update_resource(context: OperationContext, *, record_id: str | None, patch: Mapping[str, Any] | None = None, if_missing: str = "error") -> TransactionResult:
    patch = _sanitize_patch_for_scope(context, patch)
    records = load_records(context.repo_root, context.resource, tenant=context.tenant)
    chosen_id = str(record_id or patch.get("id") or synthetic_id(context.resource))
    existing = records.get(chosen_id)
    if existing is None:
        if if_missing == "skip":
            return TransactionResult(synthetic_id("txn"), context.command, context.resource, "skipped", context.dry_run, False, summary={"id": chosen_id})
        if if_missing == "create":
            return create_resource(context, record_id=chosen_id, patch=patch, if_exists="update")
        raise OperatorStateError(code=3, status="not_found", reason=f"{context.resource} {chosen_id} was not found", payload={"id": chosen_id})
    record = copy.deepcopy(existing)
    record["data"] = deep_merge(record.get("data", {}), patch)
    if patch.get("tenant") is not None:
        record["tenant"] = str(patch["tenant"])
        record.setdefault("data", {}).pop("tenant", None)
    if "status" in patch:
        record["status"] = str(patch["status"])
    if "enabled" in patch:
        record["enabled"] = bool(patch["enabled"])
    record["updated_at"] = utc_now()
    new_records = dict(records)
    new_records[chosen_id] = record
    transaction_id = _commit_records(context, records=new_records, status="updated", target_id=chosen_id, changed_ids=[chosen_id], summary={"mutation": "update"})
    return TransactionResult(transaction_id, context.command, context.resource, "updated", context.dry_run, not context.dry_run, record=record, changed_ids=[chosen_id])


def delete_resource(context: OperationContext, *, record_id: str, if_missing: str = "error") -> TransactionResult:
    records = load_records(context.repo_root, context.resource, tenant=context.tenant)
    existing = records.get(str(record_id))
    if existing is None:
        if if_missing == "skip":
            return TransactionResult(synthetic_id("txn"), context.command, context.resource, "skipped", context.dry_run, False, summary={"id": record_id})
        raise OperatorStateError(code=3, status="not_found", reason=f"{context.resource} {record_id} was not found", payload={"id": record_id})
    new_records = dict(records)
    if not context.dry_run:
        del new_records[str(record_id)]
    transaction_id = _commit_records(context, records=new_records, status="deleted", target_id=str(record_id), changed_ids=[str(record_id)], summary={"mutation": "delete"})
    return TransactionResult(transaction_id, context.command, context.resource, "deleted", context.dry_run, not context.dry_run, record=copy.deepcopy(existing), changed_ids=[str(record_id)])


def get_resource(context: OperationContext, *, record_id: str) -> TransactionResult:
    record = get_record(context.repo_root, context.resource, record_id, tenant=context.tenant)
    if record is None:
        raise OperatorStateError(code=3, status="not_found", reason=f"{context.resource} {record_id} was not found", payload={"id": record_id})
    return TransactionResult(synthetic_id("txn"), context.command, context.resource, str(record.get("status") or "ok"), context.dry_run, False, record=record)


def list_resource_result(context: OperationContext, *, status_filter: str | None = None, filter_expr: str | None = None, sort: str = "id", offset: int = 0, limit: int = 50) -> TransactionResult:
    items = _list(context.repo_root, context.resource, status_filter=status_filter, filter_expr=filter_expr, sort=sort, offset=offset, limit=limit, tenant=context.tenant)
    return TransactionResult(synthetic_id("txn"), context.command, context.resource, "ok", context.dry_run, False, items=items, summary={"offset": int(offset), "limit": int(limit)})


def toggle_resource(context: OperationContext, *, record_id: str, enabled: bool) -> TransactionResult:
    records = load_records(context.repo_root, context.resource, tenant=context.tenant)
    record = records.get(str(record_id))
    if record is None:
        raise OperatorStateError(code=3, status="not_found", reason=f"{context.resource} {record_id} was not found", payload={"id": record_id})
    patched = copy.deepcopy(record)
    patched["enabled"] = bool(enabled)
    patched["status"] = "active" if enabled else "disabled"
    patched["updated_at"] = utc_now()
    new_records = dict(records)
    new_records[str(record_id)] = patched
    transaction_id = _commit_records(context, records=new_records, status=patched["status"], target_id=str(record_id), changed_ids=[str(record_id)], summary={"mutation": "toggle", "enabled": bool(enabled)})
    return TransactionResult(transaction_id, context.command, context.resource, patched["status"], context.dry_run, not context.dry_run, record=patched, changed_ids=[str(record_id)])


def rotate_client_secret(context: OperationContext, *, record_id: str) -> TransactionResult:
    records = load_records(context.repo_root, "client", tenant=context.tenant)
    record = records.get(str(record_id))
    if record is None:
        raise OperatorStateError(code=3, status="not_found", reason=f"client {record_id} was not found", payload={"id": record_id})
    patched = copy.deepcopy(record)
    patched.setdefault("data", {})["client_secret"] = synthetic_id("client-secret")
    patched.setdefault("data", {})["client_secret_rotated_at"] = utc_now()
    patched["updated_at"] = utc_now()
    new_records = dict(records)
    new_records[str(record_id)] = patched
    transaction_id = _commit_records(context, records=new_records, status="updated", target_id=str(record_id), changed_ids=[str(record_id)], summary={"mutation": "rotate_secret"})
    return TransactionResult(transaction_id, context.command, "client", "updated", context.dry_run, not context.dry_run, record=patched, changed_ids=[str(record_id)], summary={"rotated": True})


def set_identity_password(context: OperationContext, *, record_id: str, password: str | None = None) -> TransactionResult:
    from tigrbl_identity_jose.key_management import hash_pw
    records = load_records(context.repo_root, "identity", tenant=context.tenant)
    record = records.get(str(record_id))
    if record is None:
        raise OperatorStateError(code=3, status="not_found", reason=f"identity {record_id} was not found", payload={"id": record_id})
    patched = copy.deepcopy(record)
    password = password or synthetic_id("password")
    hashed = hash_pw(password)
    patched.setdefault("data", {})["password_hash"] = hashed.decode("utf-8") if isinstance(hashed, bytes) else str(hashed)
    patched.setdefault("data", {})["password_updated_at"] = utc_now()
    patched["updated_at"] = utc_now()
    new_records = dict(records)
    new_records[str(record_id)] = patched
    transaction_id = _commit_records(context, records=new_records, status="updated", target_id=str(record_id), changed_ids=[str(record_id)], summary={"mutation": "set_password"})
    return TransactionResult(transaction_id, context.command, "identity", "updated", context.dry_run, not context.dry_run, record=patched, changed_ids=[str(record_id)])


def lock_identity(context: OperationContext, *, record_id: str, locked: bool) -> TransactionResult:
    records = load_records(context.repo_root, "identity", tenant=context.tenant)
    record = records.get(str(record_id))
    if record is None:
        raise OperatorStateError(code=3, status="not_found", reason=f"identity {record_id} was not found", payload={"id": record_id})
    patched = copy.deepcopy(record)
    patched["status"] = "locked" if locked else "active"
    patched["enabled"] = not locked
    patched.setdefault("data", {})["locked"] = bool(locked)
    patched["updated_at"] = utc_now()
    new_records = dict(records)
    new_records[str(record_id)] = patched
    transaction_id = _commit_records(context, records=new_records, status=patched["status"], target_id=str(record_id), changed_ids=[str(record_id)], summary={"mutation": "lock", "locked": bool(locked)})
    return TransactionResult(transaction_id, context.command, "identity", patched["status"], context.dry_run, not context.dry_run, record=patched, changed_ids=[str(record_id)])


def revoke_resource(context: OperationContext, *, record_id: str | None = None, status_filter: str | None = None, filter_expr: str | None = None, all_records: bool = False) -> TransactionResult:
    records = load_records(context.repo_root, context.resource, tenant=context.tenant)
    if all_records:
        ids = [str(item["id"]) for item in _list(context.repo_root, context.resource, status_filter=status_filter, filter_expr=filter_expr, sort="id", offset=0, limit=max(len(records), 1_000_000), tenant=context.tenant)]
        if not ids:
            return TransactionResult(synthetic_id("txn"), context.command, context.resource, "ok", context.dry_run, False, items=[], summary={"revoked": 0})
    else:
        if record_id is None:
            raise OperatorStateError(code=1, status="validation_error", reason="record_id is required unless all_records=True")
        ids = [str(record_id)]
    patched_records = dict(records)
    touched: list[str] = []
    for item_id in ids:
        item = patched_records.get(item_id)
        if item is None:
            if all_records:
                continue
            raise OperatorStateError(code=3, status="not_found", reason=f"{context.resource} {item_id} was not found", payload={"id": item_id})
        item = copy.deepcopy(item)
        item["status"] = "revoked"
        item["enabled"] = False
        item.setdefault("data", {})["revoked_at"] = utc_now()
        item["updated_at"] = utc_now()
        patched_records[item_id] = item
        touched.append(item_id)
    transaction_id = _commit_records(context, records=patched_records, status="revoked", target_id=touched[0] if len(touched) == 1 else None, changed_ids=touched, summary={"mutation": "revoke", "count": len(touched)})
    items = [copy.deepcopy(patched_records[item_id]) for item_id in touched]
    return TransactionResult(transaction_id, context.command, context.resource, "revoked", context.dry_run, not context.dry_run, items=items, changed_ids=touched, summary={"revoked": len(touched)})


def introspect_token_record(record: Mapping[str, Any]) -> dict[str, Any]:
    data = record.get("data") if isinstance(record.get("data"), Mapping) else {}
    return {
        "active": record.get("status") not in {"revoked", "retired", "deleted"},
        "sub": data.get("subject") or data.get("sub"),
        "client_id": data.get("client_id"),
        "scope": data.get("scope"),
        "iss": data.get("issuer") or data.get("iss"),
        "aud": data.get("audience") or data.get("aud"),
        "iat": data.get("issued_at"),
        "exp": data.get("expires_at"),
        "token_type": data.get("token_type") or data.get("kind") or "Bearer",
        "jti": data.get("jti") or record.get("id"),
        "status": record.get("status"),
    }


