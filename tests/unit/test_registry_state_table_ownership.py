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
        "AuthenticationChallenge",
        "DpopReplay",
        "DpopNonce",
        "AuthorityDerivationGraph",
        "AuthorityDerivationGraphNode",
        "AuthorityDerivationGraphEdge",
        "TrustFederationGraph",
        "TrustFederationGraphNode",
        "TrustFederationGraphEdge",
    ):
        assert name in tables.TABLE_MODEL_BY_NAME
        assert getattr(tables, name) is tables.TABLE_MODEL_BY_NAME[name]

    runtime = importlib.import_module("tigrbl_identity_storage_runtime")
    assert not hasattr(runtime, "StoragePolicyRepository")
    assert not hasattr(runtime, "StorageFederationRepository")
    assert not hasattr(runtime, "StorageInvariantRepository")
    assert not hasattr(runtime, "DpopReplayTableStore")
    assert not hasattr(runtime, "DpopNonceTableStore")


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


def test_authentication_challenge_table_is_in_migration_chain() -> None:
    migration = importlib.import_module(
        "tigrbl_identity_storage.migrations.versions.0021_authentication_challenge_table"
    )

    assert migration.down_revision == "0020_backchannel_logout_replay_table"
    assert tuple(table.__name__ for table in migration.TABLES) == (
        "AuthenticationChallenge",
    )


def test_authority_and_trust_graph_tables_are_in_migration_chain() -> None:
    migration = importlib.import_module(
        "tigrbl_identity_storage.migrations.versions.0022_authority_and_trust_graph_tables"
    )

    assert migration.down_revision == "0021_authentication_challenge_table"
    assert tuple(table.__name__ for table in migration.TABLES) == (
        "AuthorityDerivationGraph",
        "AuthorityDerivationGraphNode",
        "AuthorityDerivationGraphEdge",
        "TrustFederationGraph",
        "TrustFederationGraphNode",
        "TrustFederationGraphEdge",
    )


def test_dpop_replay_and_nonce_tables_are_in_migration_chain() -> None:
    migration = importlib.import_module(
        "tigrbl_identity_storage.migrations.versions.0034_dpop_replay_nonce_tables"
    )

    assert migration.down_revision == "0033_replay_reservations"
    assert tuple(table.__name__ for table in migration.TABLES) == (
        "DpopReplay",
        "DpopNonce",
    )


def test_dpop_table_factories_live_in_storage_runtime() -> None:
    import tigrbl_identity_storage.tables as storage
    from tigrbl_identity_storage.tables import DpopNonce, DpopReplay
    from tigrbl_identity_storage_runtime.tables.dpop import (
        DpopNonceRuntimeSpec,
        DpopReplayRuntimeSpec,
        makeDpopNonceRuntimeSpec,
        makeDpopReplayRuntimeSpec,
    )

    for legacy_name in (
        "defineDpopNonceTableSpec",
        "defineDpopReplayTableSpec",
        "deriveDpopNonceTable",
        "deriveDpopReplayTable",
        "makeDpopNonceTable",
        "makeDpopReplayTable",
        "makeInMemoryDpopNonceTable",
        "makeInMemoryDpopReplayTable",
    ):
        assert not hasattr(storage, legacy_name)

    assert DpopReplayRuntimeSpec.model is DpopReplay
    assert DpopNonceRuntimeSpec.model is DpopNonce
    assert makeDpopReplayRuntimeSpec().model is DpopReplay
    assert makeDpopNonceRuntimeSpec().model is DpopNonce
    assert {operation.alias for operation in DpopReplayRuntimeSpec.ops}.issuperset(
        {"check_and_store", "snapshot", "purge_expired", "clear"}
    )
    assert {operation.alias for operation in DpopNonceRuntimeSpec.ops}.issuperset(
        {"issue", "register", "consume", "snapshot", "purge_expired", "clear"}
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
