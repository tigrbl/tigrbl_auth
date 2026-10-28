import pytest
from pathlib import Path
import tomllib

from tba_durability_authorization_policy import normalize_legacy_authorization

ROOT = Path(__file__).resolve().parents[2]


def test_legacy_json_roles_are_normalized_to_permissions_and_tenant_grants() -> None:
    result = normalize_legacy_authorization(
        roles=[
            {"id": "r1", "tenant_id": "tenant-a", "name": "reader", "permissions": ["bucket.read"]},
        ],
        memberships=[
            {"tenant_id": "tenant-a", "principal_id": "alice", "roles": ["reader"]},
        ],
    )
    assert result.role_permissions == (("r1", "bucket.read", "allow"),)
    assert result.role_grants[0].tenant_id == "tenant-a"
    assert result.role_grants[0].resource_type == "tenant"
    assert result.role_grants[0].resource_id == "tenant-a"


def test_migration_does_not_invent_unknown_or_cross_tenant_roles() -> None:
    with pytest.raises(ValueError, match="unknown legacy role"):
        normalize_legacy_authorization(
            roles=[{"id": "r1", "tenant_id": "tenant-a", "name": "reader", "permissions": []}],
            memberships=[{"tenant_id": "tenant-b", "principal_id": "alice", "roles": ["reader"]}],
        )


def test_duplicate_role_names_fail_closed() -> None:
    with pytest.raises(ValueError, match="duplicate legacy role"):
        normalize_legacy_authorization(
            roles=[
                {"id": "r1", "tenant_id": "tenant-a", "name": "reader", "permissions": []},
                {"id": "r2", "tenant_id": "tenant-a", "name": "reader", "permissions": []},
            ],
            memberships=[],
        )


def test_normalized_schema_manifest_and_additive_migration_are_registered() -> None:
    package = ROOT / "pkgs/01-storage/tba-storage-authorization-policy"
    root_manifest = tomllib.loads((package / "component.toml").read_text(encoding="utf-8"))
    packaged_manifest = tomllib.loads((package / "src/tba_storage_authorization_policy/component.toml").read_text(encoding="utf-8"))
    assert root_manifest == packaged_manifest
    assert root_manifest["schema"]["contract"] == "1.1.0"
    physical_names = {item["physical_name"] for item in root_manifest["schema"]["objects"]}
    assert {"authn.authorization_actions", "authn.authorization_groups", "authn.authorization_group_memberships", "authn.role_permissions", "authn.role_grants", "authn.policy_approvals", "authn.policy_publications"} <= physical_names
    migration = next((package / "src/tba_storage_authorization_policy/migrations/versions").glob("*normalized_platform_iam.py")).read_text(encoding="utf-8")
    assert 'PARENT = "0ef0b038-e979-5ba7-b874-d36093292702"' in migration
    assert "checkfirst=True" in migration
