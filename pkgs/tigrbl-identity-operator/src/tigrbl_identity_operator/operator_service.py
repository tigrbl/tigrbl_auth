from __future__ import annotations

"""Production-grade durable operator service layer shared by CLI and RPC."""

import copy
import hashlib
import json
from pathlib import Path
from typing import Any, Mapping

from ._operator_store import (
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
from .authorization_provenance import (
    build_authorization_decision_trace,
    build_delegation_provenance,
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
    from .key_management import hash_pw
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


def exchange_token(context: OperationContext, *, subject_token: str | None, requested_token_type: str | None = None, audience: str | None = None, resource: str | None = None, actor_token: str | None = None, extras: Mapping[str, Any] | None = None) -> TransactionResult:
    extras_dict = dict(extras or {})
    exchange_mode = str(extras_dict.get("exchange_mode") or ("delegation" if actor_token else "impersonation"))
    subject_value = str(extras_dict.get("subject") or subject_token or "")
    actor_subject = str(extras_dict.get("actor_subject") or actor_token or "") or None
    authorization_trace = build_authorization_decision_trace(
        tenant_id=str(context.tenant or extras_dict.get("tenant_id") or ""),
        subject=subject_value,
        issuer=str(context.issuer or extras_dict.get("issuer") or ""),
        audience=audience,
        resource=resource,
        scope=str(extras_dict.get("scope") or ""),
        subject_token_type=str(extras_dict.get("subject_token_type") or "urn:ietf:params:oauth:token-type:access_token"),
        requested_token_type=str(requested_token_type or "urn:ietf:params:oauth:token-type:access_token"),
        exchange_mode=exchange_mode,
        actor_subject=actor_subject,
        source_issuer=str(extras_dict.get("source_issuer") or ""),
        sender_constraint=str(extras_dict.get("sender_constraint") or "none"),
        verifier_logic_id=str(extras_dict.get("verifier_logic_id") or "operator-token-exchange"),
        required_claims=tuple(str(item) for item in extras_dict.get("required_claims", ()) or ()),
    )
    delegation_provenance = build_delegation_provenance(
        subject_token=str(subject_token or ""),
        actor_token=str(actor_token) if actor_token else None,
        subject_claims={
            "sub": subject_value,
            "iss": str(extras_dict.get("source_issuer") or context.issuer or ""),
            "aud": audience,
        },
        actor_claims={"sub": actor_subject, "iss": str(context.issuer or "")} if actor_subject else None,
        authorization_trace=authorization_trace,
        audience=audience,
        resource=resource,
        exchange_mode=exchange_mode,
        sender_constraint=str(extras_dict.get("sender_constraint") or "none"),
    )
    token_id = synthetic_id("token")
    patch = {
        "subject_token": subject_token,
        "actor_token": actor_token,
        "requested_token_type": requested_token_type or "urn:ietf:params:oauth:token-type:access_token",
        "audience": audience,
        "resource": resource,
        "issued_at": utc_now(),
        "claims": {
            "authorization_trace": authorization_trace,
            "delegation_provenance": delegation_provenance,
        },
        **extras_dict,
    }
    return create_resource(context, record_id=token_id, patch=patch, if_exists="error")


def generate_key_record(context: OperationContext, *, patch: Mapping[str, Any] | None = None) -> TransactionResult:
    patch = _sanitize_patch_for_scope(context, patch)
    patch.setdefault("kid", synthetic_id("kid"))
    patch.setdefault("alg", patch.get("alg") or "EdDSA")
    patch.setdefault("use", patch.get("use") or "sig")
    patch.setdefault("kty", patch.get("kty") or "OKP")
    patch.setdefault("curve", patch.get("curve") or "Ed25519")
    return create_resource(context, record_id=patch["kid"], patch=patch, if_exists="error")


def rotate_key_record(context: OperationContext, *, record_id: str) -> TransactionResult:
    records = load_records(context.repo_root, "keys", tenant=context.tenant)
    record = records.get(str(record_id))
    if record is None:
        raise OperatorStateError(code=3, status="not_found", reason=f"keys {record_id} was not found", payload={"id": record_id})
    patched = copy.deepcopy(record)
    patched["status"] = "active"
    patched["enabled"] = True
    patched.setdefault("data", {})["rotated_at"] = utc_now()
    patched["updated_at"] = utc_now()
    new_records = dict(records)
    new_records[str(record_id)] = patched
    transaction_id = _commit_records(context, records=new_records, status="updated", target_id=str(record_id), changed_ids=[str(record_id)], summary={"mutation": "rotate_key"})
    return TransactionResult(transaction_id, context.command, "keys", "updated", context.dry_run, not context.dry_run, record=patched, changed_ids=[str(record_id)])


def retire_key_record(context: OperationContext, *, record_id: str, retire_after: str | None = None) -> TransactionResult:
    records = load_records(context.repo_root, "keys", tenant=context.tenant)
    record = records.get(str(record_id))
    if record is None:
        raise OperatorStateError(code=3, status="not_found", reason=f"keys {record_id} was not found", payload={"id": record_id})
    patched = copy.deepcopy(record)
    patched["status"] = "retired"
    patched["enabled"] = False
    patched.setdefault("data", {})["retired_at"] = utc_now()
    if retire_after:
        patched.setdefault("data", {})["retire_after"] = retire_after
    patched["updated_at"] = utc_now()
    new_records = dict(records)
    new_records[str(record_id)] = patched
    transaction_id = _commit_records(context, records=new_records, status="retired", target_id=str(record_id), changed_ids=[str(record_id)], summary={"mutation": "retire_key"})
    return TransactionResult(transaction_id, context.command, "keys", "retired", context.dry_run, not context.dry_run, record=patched, changed_ids=[str(record_id)])


def _key_publication_status(record: Mapping[str, Any]) -> str:
    data = record.get("data") or {}
    if isinstance(data, Mapping):
        explicit = data.get("publication_status")
        if explicit not in {None, ""}:
            return str(explicit).lower()
    return str(record.get("status") or "").lower()


def key_is_publicly_publishable(record: Mapping[str, Any], *, include_retired: bool = False) -> bool:
    data = record.get("data") or {}
    if not isinstance(data, Mapping):
        data = {}
    if data.get("publish") is False:
        return False
    if str(record.get("status") or "").lower() in {"deleted", "disabled", "revoked"}:
        return False
    status_value = _key_publication_status(record)
    if status_value in {"active", "next"}:
        return True
    if status_value == "retired":
        return bool(include_retired or data.get("publish_retired") is True or data.get("publish") is True)
    return bool(data.get("publish") is True or data.get("public") is True)


def operator_jwks_key(record: Mapping[str, Any]) -> dict[str, Any]:
    data = record.get("data") or {}
    if not isinstance(data, Mapping):
        data = {}
    key: dict[str, Any] = {
        "kid": str(data.get("kid") or record.get("id")),
        "alg": str(data.get("alg") or "EdDSA"),
        "use": str(data.get("use") or "sig"),
        "kty": str(data.get("kty") or "OKP"),
        "crv": str(data.get("crv") or data.get("curve") or "Ed25519"),
        "status": _key_publication_status(record),
    }
    for field in ("x", "n", "e"):
        if data.get(field) not in {None, ""}:
            key[field] = str(data[field])
    return key


def build_operator_jwks_payload(repo_root: Path, *, tenant: str | None = None) -> dict[str, Any]:
    keys = _list(repo_root, "keys", sort="id", offset=0, limit=1000, tenant=tenant)
    return {"keys": [operator_jwks_key(item) for item in keys if key_is_publicly_publishable(item, include_retired=tenant is None)]}


def publish_jwks_document(context: OperationContext, *, output_path: str | None = None) -> ArtifactResult:
    jwks = build_operator_jwks_payload(context.repo_root, tenant=context.tenant)
    if output_path:
        path = Path(output_path)
    elif context.tenant:
        path = context.repo_root / "dist" / "jwks" / "tenants" / context.tenant / "jwks.json"
    else:
        path = context.repo_root / "dist" / "jwks" / "jwks.json"
    write_structured(path, jwks)
    return ArtifactResult(command=context.command, resource=context.resource, status="published", path=display_path(path, context.repo_root), checksum=validate_checksum(path), summary={"keys": len(jwks["keys"]), "profile": context.profile, "tenant": context.tenant})


def build_portability_artifact(repo_root: Path, *, include_resources: list[str] | None = None, redact: bool = False, tenant: str | None = None) -> dict[str, Any]:
    include_resources = include_resources or sorted(GENERIC_RESOURCES)
    resources: dict[str, Any] = {}
    per_resource_checksums: dict[str, str] = {}
    for resource in include_resources:
        records = _list(repo_root, resource, sort="id", offset=0, limit=100000, tenant=tenant)
        if redact:
            redacted_records = []
            for record in records:
                copy_record = copy.deepcopy(record)
                data = copy_record.get("data") or {}
                if isinstance(data, Mapping):
                    for secret_key in ("client_secret", "password_hash", "token"):
                        if secret_key in data:
                            data[secret_key] = "<redacted>"
                redacted_records.append(copy_record)
            records = redacted_records
        resources[resource] = records
        per_resource_checksums[resource] = hashlib.sha256(json.dumps(records, sort_keys=True).encode("utf-8")).hexdigest()
    payload = {
        "schema_version": PORTABILITY_SCHEMA_VERSION,
        "generated_at": utc_now(),
        "storage_backend": "sqlite-authoritative",
        "tenant_scope": tenant,
        "resources": resources,
        "resource_checksums": per_resource_checksums,
        "resource_versions": {resource: max((int(item.get("revision") or 0) for item in records), default=0) for resource, records in resources.items()},
    }
    payload["checksum"] = hashlib.sha256(json.dumps(payload["resources"], sort_keys=True).encode("utf-8")).hexdigest()
    return payload


def validate_import_artifact(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    resources = payload.get("resources", {})
    computed = hashlib.sha256(json.dumps(resources, sort_keys=True).encode("utf-8")).hexdigest()
    valid_version = int(payload.get("schema_version") or 0) >= PORTABILITY_SCHEMA_VERSION
    valid_backend = str(payload.get("storage_backend") or "") in {"sqlite-authoritative", ""}
    return {
        "valid": computed == payload.get("checksum") and valid_version and valid_backend,
        "declared_checksum": payload.get("checksum"),
        "computed_checksum": computed,
        "resource_count": len(resources),
        "resources": sorted(resources.keys()),
        "schema_version": int(payload.get("schema_version") or 0),
        "storage_backend": payload.get("storage_backend"),
        "tenant_scope": payload.get("tenant_scope"),
        "resource_versions": payload.get("resource_versions", {}),
    }


def run_import(context: OperationContext, *, path: Path) -> ArtifactResult:
    validation = validate_import_artifact(path)
    if not validation["valid"]:
        raise OperatorStateError(code=4, status="validation_error", reason="import checksum mismatch", payload=validation)
    payload = json.loads(path.read_text(encoding="utf-8"))
    imported = 0
    for resource, records in payload.get("resources", {}).items():
        existing = load_records(context.repo_root, resource, tenant=context.tenant)
        new_records = dict(existing)
        for item in records:
            if not isinstance(item, Mapping):
                continue
            record_id = str(item.get("id") or synthetic_id(resource))
            incoming = copy.deepcopy(dict(item))
            if context.tenant is not None:
                incoming["tenant"] = context.tenant
            new_records[record_id] = incoming
            imported += 1
        context_resource = OperationContext(context.repo_root, context.command, resource, dry_run=context.dry_run, actor=context.actor, profile=context.profile, tenant=context.tenant, issuer=context.issuer)
        _commit_records(context_resource, records=new_records, status="imported", target_id=None, changed_ids=list(new_records.keys()), summary={"mutation": "import", "count": len(records), "schema_version": validation.get("schema_version"), "storage_backend": validation.get("storage_backend")})
    return ArtifactResult(command=context.command, resource=context.resource, status="imported", path=display_path(path, context.repo_root), checksum=validation["computed_checksum"], summary={"imported_records": imported, "resources": validation["resources"], "schema_version": validation.get("schema_version"), "storage_backend": validation.get("storage_backend")})


def run_export(context: OperationContext, *, output_path: Path, redact: bool = False) -> ArtifactResult:
    payload = build_portability_artifact(context.repo_root, redact=redact, tenant=context.tenant)
    write_structured(output_path, payload)
    return ArtifactResult(command=context.command, resource=context.resource, status="exported", path=display_path(output_path, context.repo_root), checksum=validate_checksum(output_path), summary={"resources": sorted(payload["resources"].keys()), "redacted": redact})


def import_status(repo_root: Path) -> dict[str, Any]:
    event = latest_event(repo_root, predicate=lambda item: item.get("details", {}).get("source_surface") == "import-export" and item.get("event_type") == "import")
    return {"last_import": event, "operator_plane": operator_store_summary(repo_root)}


def export_status(repo_root: Path) -> dict[str, Any]:
    event = latest_event(repo_root, predicate=lambda item: item.get("details", {}).get("source_surface") == "import-export" and item.get("event_type") == "export")
    return {"last_export": event, "operator_plane": operator_store_summary(repo_root)}


def operator_plane_status(repo_root: Path) -> dict[str, Any]:
    summary = operator_store_summary(repo_root)
    summary["resource_count"] = sum(len(load_records(repo_root, resource)) for resource in sorted(GENERIC_RESOURCES))
    summary["tracked_resources"] = sorted(GENERIC_RESOURCES)
    summary["last_import"] = import_status(repo_root).get("last_import")
    summary["last_export"] = export_status(repo_root).get("last_export")
    return summary


def list_transactions(repo_root: Path) -> list[dict[str, Any]]:
    return read_jsonl(transaction_log_path(repo_root))


def list_audit_rows(repo_root: Path) -> list[dict[str, Any]]:
    return read_jsonl(audit_log_path(repo_root))


def list_activity(repo_root: Path) -> list[dict[str, Any]]:
    return read_jsonl(activity_log_path(repo_root))


__all__ = [
    "ArtifactResult",
    "GENERIC_RESOURCES",
    "OperationContext",
    "OperatorStateError",
    "TransactionResult",
    "build_operator_jwks_payload",
    "build_portability_artifact",
    "create_resource",
    "delete_resource",
    "exchange_token",
    "export_status",
    "generate_key_record",
    "get_record",
    "get_resource",
    "import_status",
    "introspect_token_record",
    "list_activity",
    "operator_plane_status",
    "list_audit_rows",
    "list_resource",
    "list_resource_result",
    "list_transactions",
    "lock_identity",
    "publish_jwks_document",
    "retire_key_record",
    "revoke_resource",
    "rotate_client_secret",
    "rotate_key_record",
    "run_export",
    "run_import",
    "set_identity_password",
    "toggle_resource",
    "update_resource",
    "validate_import_artifact",
]
