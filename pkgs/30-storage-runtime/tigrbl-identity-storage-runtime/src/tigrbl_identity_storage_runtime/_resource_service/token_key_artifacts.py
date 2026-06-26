from __future__ import annotations
# ruff: noqa: F403,F405

import hashlib
import json

from .resource_operations import *
from .resource_operations import _commit_records, _list, _sanitize_patch_for_scope
from tigrbl_identity_storage_runtime.operator_store import (
    ArtifactResult,
    PORTABILITY_SCHEMA_VERSION,
    activity_log_path,
    audit_log_path,
    display_path,
    latest_event,
    operator_store_summary,
    read_jsonl,
    transaction_log_path,
    validate_checksum,
    write_structured,
)
from tigrbl_security_authorization_provenance_builder import (
    build_authorization_decision_trace,
    build_delegation_provenance,
)

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
    "key_is_publicly_publishable",
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
