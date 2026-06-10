from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Mapping

from ._operator_store import ArtifactResult, display_path, latest_event, read_jsonl, validate_checksum, write_structured
from .operator_service import list_activity, list_audit_rows, list_transactions


def record_surface_event(
    repo_root: Path,
    *,
    event_type: str,
    target_type: str,
    target_id: str | None,
    outcome: str,
    tenant_id: str | None = None,
    actor_user_id: str | None = None,
    actor_client_id: str | None = None,
    session_id: str | None = None,
    details: Mapping[str, Any] | None = None,
    source_surface: str = "operator",
) -> dict[str, Any]:
    from ._operator_store import OperationContext, build_audit_entry, append_jsonl, audit_log_path, utc_now

    context = OperationContext(repo_root=repo_root, command=event_type, resource=target_type, dry_run=False, actor=actor_user_id or "system", tenant=tenant_id)
    entry = build_audit_entry(
        context,
        transaction_id=hashlib.sha256(json.dumps({"event_type": event_type, "target_id": target_id, "occurred_at": utc_now()}, sort_keys=True).encode("utf-8")).hexdigest()[:16],
        status=outcome,
        target_id=target_id,
        details={**dict(details or {}), "source_surface": source_surface, "actor_client_id": actor_client_id, "session_id": session_id},
        source_surface=source_surface,
    )
    append_jsonl(audit_log_path(repo_root), entry)
    return entry


def list_audit_events(repo_root: Path) -> list[dict[str, Any]]:
    return list_audit_rows(repo_root)


def export_audit_events(repo_root: Path, *, output_path: Path | None = None) -> ArtifactResult:
    output_path = output_path or (repo_root / "dist" / "audit" / "audit_events.json")
    payload = {
        "transactions": list_transactions(repo_root),
        "audit_events": list_audit_rows(repo_root),
        "activity": list_activity(repo_root),
    }
    write_structured(output_path, payload)
    return ArtifactResult(command="audit", resource="audit", status="exported", path=display_path(output_path, repo_root), checksum=validate_checksum(output_path), summary={"transactions": len(payload["transactions"]), "audit_events": len(payload["audit_events"]), "activity": len(payload["activity"])})


def latest_audit_event(repo_root: Path, *, target_type: str | None = None) -> dict[str, Any] | None:
    if target_type is None:
        return latest_event(repo_root)
    return latest_event(repo_root, predicate=lambda item: item.get("target_type") == target_type)


__all__ = [
    "export_audit_events",
    "latest_audit_event",
    "list_audit_events",
    "record_surface_event",
]
