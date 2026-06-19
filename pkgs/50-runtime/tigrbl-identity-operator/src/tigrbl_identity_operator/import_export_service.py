from __future__ import annotations

from pathlib import Path

from ._operator_store import ArtifactResult, OperationContext, PORTABILITY_SCHEMA_VERSION
from .audit_service import record_surface_event
from .operator_service import export_status, import_status, operator_plane_status, run_export, run_import, validate_import_artifact


def validate_import_file(path: Path) -> dict[str, object]:
    return validate_import_artifact(path)


def run_import_file(context: OperationContext, *, path: Path) -> ArtifactResult:
    result = run_import(context, path=path)
    record_surface_event(context.repo_root, event_type="import", target_type="artifact", target_id=result.checksum, outcome=result.status, tenant_id=context.tenant, actor_user_id=context.actor, details=result.to_payload(), source_surface="import-export")
    return result


def validate_export_plan(context: OperationContext, *, redact: bool = False) -> dict[str, object]:
    return {"valid": True, "profile": context.profile, "redacted": redact, "schema_version": PORTABILITY_SCHEMA_VERSION, "operator_plane": operator_plane_status(context.repo_root)}


def run_export_file(context: OperationContext, *, path: Path, redact: bool = False) -> ArtifactResult:
    result = run_export(context, output_path=path, redact=redact)
    record_surface_event(context.repo_root, event_type="export", target_type="artifact", target_id=result.checksum, outcome=result.status, tenant_id=context.tenant, actor_user_id=context.actor, details=result.to_payload(), source_surface="import-export")
    return result


__all__ = [
    "export_status",
    "import_status",
    "run_export_file",
    "run_import_file",
    "validate_export_plan",
    "validate_import_file",
]
