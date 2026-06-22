from __future__ import annotations

from pathlib import Path

from tigrbl_identity_storage.operator_store import OperationContext, operator_store_summary
from tigrbl_identity_storage.resource_service import (
    create_resource,
    delete_resource,
    generate_key_record,
    get_resource,
    list_resource_result,
    publish_jwks_document,
    run_export,
    run_import,
    update_resource,
    validate_import_artifact,
)
from tigrbl_identity_storage.session_service import observe_token_response, token_hash
from tigrbl_auth_protocol_oidc.discovery_service import diff_discovery, show_discovery
from tigrbl_identity_storage.portability import validate_export_plan


def _context(repo_root: Path, resource: str, command: str) -> OperationContext:
    return OperationContext(repo_root=repo_root, command=command, resource=resource, actor="unit", profile="baseline")


def test_operator_service_layer_round_trip(tmp_path: Path) -> None:
    tenant_ctx = _context(tmp_path, "tenant", "tenant.create")
    create = create_resource(tenant_ctx, record_id="tenant-a", patch={"name": "Tenant A"}, if_exists="error")
    assert create.status == "created"
    assert create.record and create.record["data"]["name"] == "Tenant A"

    update = update_resource(_context(tmp_path, "tenant", "tenant.update"), record_id="tenant-a", patch={"display_name": "Tenant Alpha"}, if_missing="error")
    assert update.status == "updated"
    fetched = get_resource(_context(tmp_path, "tenant", "tenant.get"), record_id="tenant-a")
    assert fetched.record and fetched.record["data"]["display_name"] == "Tenant Alpha"

    keys_ctx = _context(tmp_path, "keys", "keys.generate")
    key = generate_key_record(keys_ctx, patch={"kid": "kid-1", "label": "primary"})
    assert key.record and key.record["id"] == "kid-1"
    jwks = publish_jwks_document(_context(tmp_path, "keys", "keys.publish"))
    assert jwks.status == "published"

    export_path = tmp_path / "export.json"
    export_result = run_export(_context(tmp_path, "export", "export.run"), output_path=export_path, redact=True)
    assert export_result.status == "exported"
    validation = validate_import_artifact(export_path)
    assert validation["valid"] is True

    imported_root = tmp_path / "imported"
    import_result = run_import(_context(imported_root, "import", "import.run"), path=export_path)
    assert import_result.status == "imported"
    imported = get_resource(_context(imported_root, "tenant", "tenant.get"), record_id="tenant-a")
    assert imported.record and imported.record["data"]["display_name"] == "Tenant Alpha"

    delete = delete_resource(_context(imported_root, "tenant", "tenant.delete"), record_id="tenant-a")
    assert delete.status == "deleted"


def test_runtime_observation_and_discovery(repo_root: Path | None = None) -> None:
    repo_root = Path(repo_root or Path(__file__).resolve().parents[2])
    temp_root = repo_root / "dist" / "capability-test-observation"
    temp_root.mkdir(parents=True, exist_ok=True)
    observe = observe_token_response(temp_root, access_token="abc.def.ghi", details={"subject": "user-1", "scope": "openid"})
    assert observe["access_token_id"] == token_hash("abc.def.ghi")
    listing = list_resource_result(_context(temp_root, "token", "token.list"), limit=10, offset=0)
    assert listing.items and listing.items[0]["id"] == token_hash("abc.def.ghi")

    export_plan = validate_export_plan(_context(temp_root, "export", "export.validate"), redact=True)
    assert export_plan["valid"] is True
    assert export_plan["schema_version"] >= 3
    summary = operator_store_summary(temp_root)
    assert summary["backend"] == "sqlite-authoritative"
    assert summary["repo_mutation_dependency"] is False

    discovery = show_discovery(Path(__file__).resolve().parents[2], profile="baseline")
    assert "openid-configuration.json" in discovery["documents"]
    diff = diff_discovery(Path(__file__).resolve().parents[2], left_profile="baseline", right_profile="production")
    assert diff["document_count"] >= 1
