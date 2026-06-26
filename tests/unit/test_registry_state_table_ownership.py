from __future__ import annotations

import importlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def test_registry_state_has_storage_tables_and_runtime_repositories() -> None:
    tables = importlib.import_module("tigrbl_identity_storage.tables")
    runtime = importlib.import_module("tigrbl_identity_storage_runtime")

    for name in (
        "IdentityProvider",
        "FederatedSession",
        "AuthorizationInvariant",
        "InvariantEvaluation",
        "InvariantViolation",
    ):
        assert name in tables.TABLE_MODEL_BY_NAME
        assert getattr(tables, name) is tables.TABLE_MODEL_BY_NAME[name]

    assert hasattr(runtime, "StoragePolicyRepository")
    assert hasattr(runtime, "StorageFederationRepository")
    assert hasattr(runtime, "StorageInvariantRepository")
    assert hasattr(runtime, "create_storage_policy_repository")
    assert hasattr(runtime, "create_storage_federation_repository")
    assert hasattr(runtime, "create_storage_invariant_repository")


def test_registry_tables_are_in_migration_chain() -> None:
    migration = importlib.import_module(
        "tigrbl_identity_storage.migrations.versions.0019_federation_and_invariant_tables"
    )

    assert migration.down_revision == "0018_policy_repository_tables"
    assert tuple(table.__name__ for table in migration.TABLES) == (
        "IdentityProvider",
        "FederatedSession",
        "AuthorizationInvariant",
        "InvariantEvaluation",
        "InvariantViolation",
    )


def test_concrete_state_registries_are_marked_for_compatibility_only() -> None:
    concrete_modules = {
        "tigrbl_identity_admin_policy_registry": "PolicyRegistry",
        "tigrbl_identity_admin_federation_registry": "FederationRegistry",
        "tigrbl_authz_policy_invariant_registry": "InvariantRegistry",
    }
    runtime_modules = {
        "tigrbl_identity_storage_runtime.policy_repository": "StoragePolicyRepository",
        "tigrbl_identity_storage_runtime.federation_repository": "StorageFederationRepository",
        "tigrbl_identity_storage_runtime.invariant_repository": "StorageInvariantRepository",
    }

    for module_name, class_name in concrete_modules.items():
        module = importlib.import_module(module_name)
        assert hasattr(module, class_name)

    for module_name, class_name in runtime_modules.items():
        module = importlib.import_module(module_name)
        assert hasattr(module, class_name)
