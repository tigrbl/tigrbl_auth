from __future__ import annotations

import json
from pathlib import Path

import pytest

from tigrbl_auth.services._operator_store import OperationContext, operator_state_root, operator_store_summary
from tigrbl_auth.cli.handlers import _operator_state_dir
from tigrbl_auth.services.import_export_service import validate_export_plan
from tigrbl_auth.services.operator_service import OperatorStateError, build_portability_artifact, create_resource, get_resource, list_resource_result, update_resource


def _ctx(repo_root: Path, resource: str, command: str, *, tenant: str | None = None) -> OperationContext:
    return OperationContext(repo_root=repo_root, command=command, resource=resource, actor="unit", profile="production", tenant=tenant)


def test_operator_plane_uses_durable_external_sqlite_backend(tmp_path: Path) -> None:
    repo_root = tmp_path / "repo"
    repo_root.mkdir()
    result = create_resource(_ctx(repo_root, "tenant", "tenant.create", tenant="tenant-a"), record_id="tenant-a", patch={"name": "Tenant A"})
    assert result.status == "created"

    state_root = operator_state_root(repo_root)
    summary = operator_store_summary(repo_root)
    assert (state_root / "operator_plane.sqlite3").exists()
    assert summary["backend"] == "sqlite-authoritative"
    assert summary["repo_mutation_dependency"] is False
    assert summary["tenancy_enforced"] is True
    assert repo_root.resolve() not in state_root.resolve().parents


def test_operator_plane_enforces_tenant_boundaries_and_versioned_export(tmp_path: Path) -> None:
    repo_root = tmp_path / "repo"
    repo_root.mkdir()
    create_resource(_ctx(repo_root, "client", "client.create", tenant="tenant-a"), record_id="client-a", patch={"name": "Client A"})
    create_resource(_ctx(repo_root, "client", "client.create", tenant="tenant-b"), record_id="client-b", patch={"name": "Client B"})

    items_a = list_resource_result(_ctx(repo_root, "client", "client.list", tenant="tenant-a")).items or []
    items_b = list_resource_result(_ctx(repo_root, "client", "client.list", tenant="tenant-b")).items or []
    assert [item["id"] for item in items_a] == ["client-a"]
    assert [item["id"] for item in items_b] == ["client-b"]

    with pytest.raises(OperatorStateError):
        get_resource(_ctx(repo_root, "client", "client.get", tenant="tenant-a"), record_id="client-b")

    artifact = build_portability_artifact(repo_root, tenant="tenant-a", redact=False)
    assert artifact["schema_version"] >= 3
    assert artifact["storage_backend"] == "sqlite-authoritative"
    assert artifact["tenant_scope"] == "tenant-a"
    assert sorted(artifact["resources"]["client"][0].keys())
    plan = validate_export_plan(_ctx(repo_root, "export", "export.validate", tenant="tenant-a"), redact=True)
    assert plan["schema_version"] >= 3
    assert plan["operator_plane"]["repo_mutation_dependency"] is False

    update = update_resource(_ctx(repo_root, "client", "client.update", tenant="tenant-a"), record_id="client-a", patch={"display_name": "Client Alpha"})
    assert update.record is not None
    assert int(update.record.get("revision") or 0) >= 1


def test_cli_handler_status_root_is_external_to_repo(tmp_path: Path) -> None:
    repo_root = tmp_path / "repo"
    repo_root.mkdir()
    state_dir = _operator_state_dir(repo_root)
    assert state_dir.name == "status"
    assert repo_root.resolve() not in state_dir.resolve().parents

