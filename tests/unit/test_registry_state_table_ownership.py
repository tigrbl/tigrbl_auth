from __future__ import annotations

import importlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def test_registry_state_has_storage_tables_without_runtime_repositories() -> None:
    tables = importlib.import_module("tigrbl_identity_storage.tables")

    for name in (
        "Policy",
        "IdentityProvider",
        "Federation",
        "FederatedSession",
        "AuthorizationInvariant",
        "InvariantEvaluation",
        "InvariantViolation",
        "BackchannelLogoutReplay",
    ):
        assert name in tables.TABLE_MODEL_BY_NAME
        assert getattr(tables, name) is tables.TABLE_MODEL_BY_NAME[name]

    runtime = importlib.import_module("tigrbl_identity_storage_runtime")
    assert not hasattr(runtime, "StoragePolicyRepository")
    assert not hasattr(runtime, "StorageFederationRepository")
    assert not hasattr(runtime, "StorageInvariantRepository")


def test_registry_tables_are_in_migration_chain() -> None:
    migration = importlib.import_module(
        "tigrbl_identity_storage.migrations.versions.0019_federation_and_invariant_tables"
    )

    assert migration.down_revision == "0018_policy_tables"
    assert tuple(table.__name__ for table in migration.TABLES) == (
        "IdentityProvider",
        "Federation",
        "FederatedSession",
        "AuthorizationInvariant",
        "InvariantEvaluation",
        "InvariantViolation",
    )


def test_backchannel_replay_table_is_in_migration_chain() -> None:
    migration = importlib.import_module(
        "tigrbl_identity_storage.migrations.versions.0020_backchannel_logout_replay_table"
    )

    assert migration.down_revision == "0019_federation_and_invariant_tables"
    assert tuple(table.__name__ for table in migration.TABLES) == (
        "BackchannelLogoutReplay",
    )


def test_deprecated_state_registries_are_marked_for_compatibility_only() -> None:
    compatibility_modules = {
        "tigrbl_identity_admin_policy_registry": "PolicyRegistry",
        "tigrbl_identity_admin_federation_registry": "FederationRegistry",
        "tigrbl_authz_policy_invariant_registry": "InvariantRegistry",
    }
    for module_name, class_name in compatibility_modules.items():
        module = importlib.import_module(module_name)
        assert hasattr(module, class_name)

    for removed_module in (
        "tigrbl_identity_storage_runtime.policy_repository",
        "tigrbl_identity_storage_runtime.federation_repository",
        "tigrbl_identity_storage_runtime.invariant_repository",
    ):
        try:
            importlib.import_module(removed_module)
        except ModuleNotFoundError:
            continue
        raise AssertionError(f"{removed_module} should not define a registry repository wrapper")
