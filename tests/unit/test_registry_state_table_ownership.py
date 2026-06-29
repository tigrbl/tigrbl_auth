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
        "tigrbl_identity_storage.migrations.versions.0023_dpop_replay_nonce_tables"
    )

    assert migration.down_revision == "0022_authority_and_trust_graph_tables"
    assert tuple(table.__name__ for table in migration.TABLES) == (
        "DpopReplay",
        "DpopNonce",
    )


def test_dpop_tables_expose_define_derive_make_factories() -> None:
    from tigrbl.factories.engine import mem, sqlitef
    from tigrbl_identity_storage.tables import DpopNonce, DpopReplay
    from tigrbl_identity_dpop_state_concrete import (
        defineDpopNonceTableSpec,
        defineDpopReplayTableSpec,
        deriveDpopNonceTable,
        deriveDpopReplayTable,
        makeDpopNonceTable,
        makeDpopReplayTable,
        makeInMemoryDpopNonceTable,
        makeInMemoryDpopReplayTable,
    )

    replay_spec = defineDpopReplayTableSpec(engine=mem(async_=False))
    nonce_spec = defineDpopNonceTableSpec(engine=mem(async_=False))
    assert replay_spec.table_config["engine"] == mem(async_=False)
    assert nonce_spec.table_config["engine"] == mem(async_=False)

    derived_replay = deriveDpopReplayTable(class_name="DerivedDpopReplayForTest", engine=mem(async_=False))
    derived_nonce = deriveDpopNonceTable(class_name="DerivedDpopNonceForTest", engine=mem(async_=False))
    assert issubclass(derived_replay, DpopReplay)
    assert issubclass(derived_nonce, DpopNonce)
    assert derived_replay.__table__ is DpopReplay.__table__
    assert derived_nonce.__table__ is DpopNonce.__table__
    assert derived_replay.table_config["engine"] == mem(async_=False)
    assert derived_nonce.table_config["engine"] == mem(async_=False)

    durable_replay = makeDpopReplayTable(
        class_name="DurableDpopReplayForTest",
        engine=sqlitef("dpop-replay.db", async_=False),
    )
    durable_nonce = makeDpopNonceTable(
        class_name="DurableDpopNonceForTest",
        engine=sqlitef("dpop-nonce.db", async_=False),
    )
    assert durable_replay.table_config["engine"] == sqlitef("dpop-replay.db", async_=False)
    assert durable_nonce.table_config["engine"] == sqlitef("dpop-nonce.db", async_=False)

    memory_replay = makeInMemoryDpopReplayTable(class_name="InMemoryDpopReplayForTest", async_=False)
    memory_nonce = makeInMemoryDpopNonceTable(class_name="InMemoryDpopNonceForTest", async_=False)
    assert memory_replay.table_config["engine"] == mem(async_=False)
    assert memory_nonce.table_config["engine"] == mem(async_=False)
    assert memory_replay.__table__ is DpopReplay.__table__
    assert memory_nonce.__table__ is DpopNonce.__table__


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
