from __future__ import annotations

import importlib
import pkgutil
from pathlib import Path
from importlib.resources import as_file, files

import pytest
from sqlalchemy import create_engine, inspect

from tigrbl_identity_storage.components import COMPONENT_IMPORT_ROOTS, load_full_composition
from tigrbl_identity_storage.tables import TABLE_MODELS as COMPATIBILITY_MODELS
from tigrbl_migrations import DeploymentLock, MigrationLedger, MigrationOrchestrator


def _model_inventory():
    composition, migrations = load_full_composition()
    models = []
    for manifest in composition.manifests:
        module = importlib.import_module(manifest.import_root)
        models.extend(module.TABLE_MODELS)
    return composition, migrations, tuple(models)


def _sqlite_connection():
    engine = create_engine("sqlite+pysqlite:///:memory:")
    connection = engine.connect()
    connection.exec_driver_sql("ATTACH DATABASE ':memory:' AS authn")
    return engine, connection


def _schema_signature(connection):
    inspector = inspect(connection)
    signature = {}
    for schema in (None, "authn"):
        for table in sorted(inspector.get_table_names(schema=schema)):
            if table == "schema_migrations" or table.startswith("tigrbl_schema_"):
                continue
            qualified = f"{schema}.{table}" if schema else table
            signature[qualified] = tuple(
                sorted(
                    (
                        column["name"],
                        str(column["type"]),
                        bool(column["nullable"]),
                        repr(column.get("default")),
                    )
                    for column in inspector.get_columns(table, schema=schema)
                )
            )
    return signature


def test_all_tables_have_one_component_identity_and_one_object_identity() -> None:
    composition, migrations, models = _model_inventory()
    objects = [owned for manifest in composition.manifests for owned in manifest.objects]
    assert len(composition.manifests) == 29
    assert len(migrations) == 29
    assert len(models) == 153
    assert len(COMPATIBILITY_MODELS) == 153
    assert {id(model) for model in models} == {id(model) for model in COMPATIBILITY_MODELS}
    assert len({owned.id for owned in objects}) == 153
    assert len({owned.physical_name for owned in objects}) == 153
    assert {owned.physical_name for owned in objects} == {
        model.__table__.fullname for model in models
    }


def test_component_dependencies_cover_every_cross_component_foreign_key() -> None:
    composition, _migrations, models = _model_inventory()
    owner = {
        owned.physical_name: manifest.component_id
        for manifest in composition.manifests
        for owned in manifest.objects
    }
    requirements = {
        manifest.component_id: {item.component for item in manifest.requires}
        for manifest in composition.manifests
    }
    for model in models:
        source_owner = owner[model.__table__.fullname]
        for foreign_key in model.__table__.foreign_keys:
            target_name = foreign_key.target_fullname.rsplit(".", 1)[0]
            if target_name.count(".") == 0:
                target_name = "authn." + target_name
            target_owner = owner[target_name]
            if target_owner != source_owner:
                assert target_owner in requirements[source_owner], (
                    model.__table__.fullname,
                    target_name,
                    source_owner,
                    target_owner,
                )


def test_fresh_component_install_is_repeatable_and_records_ownership() -> None:
    composition, migrations, _models = _model_inventory()
    engine, connection = _sqlite_connection()
    try:
        ledger = MigrationLedger(connection)
        versions = {manifest.component_id: "0.4.0.dev2" for manifest in composition.manifests}
        orchestrator = MigrationOrchestrator(composition, migrations, ledger, versions)
        first = orchestrator.apply()
        second = orchestrator.apply()
        assert len(first.ordered) == 29
        assert not second.ordered
        assert len(_schema_signature(connection)) == 153
        ownership = connection.exec_driver_sql(
            "SELECT COUNT(*) FROM tigrbl_schema_ownership WHERE ownership_state = 'active'"
        ).scalar_one()
        assert ownership == 153
    finally:
        connection.close()
        engine.dispose()


def test_frozen_monolith_upgrade_matches_fresh_component_schema() -> None:
    composition, migrations, _models = _model_inventory()
    fresh_engine, fresh = _sqlite_connection()
    legacy_engine, legacy = _sqlite_connection()
    try:
        versions = {manifest.component_id: "0.4.0.dev2" for manifest in composition.manifests}
        MigrationOrchestrator(
            composition, migrations, MigrationLedger(fresh), versions
        ).apply()
        versions_package = importlib.import_module(
            "tigrbl_identity_storage.migrations.versions"
        )
        modules = [
            importlib.import_module(module.name)
            for module in pkgutil.iter_modules(
                versions_package.__path__, versions_package.__name__ + "."
            )
            if not module.name.rsplit(".", 1)[-1].startswith("0038_")
        ]
        for module in sorted(modules, key=lambda value: value.revision):
            module.upgrade(legacy)
        assert _schema_signature(legacy) == _schema_signature(fresh)
    finally:
        fresh.close()
        legacy.close()
        fresh_engine.dispose()
        legacy_engine.dispose()


def test_legacy_adoption_preserves_data_and_claims_every_object(monkeypatch) -> None:
    engine, connection = _sqlite_connection()
    try:
        versions_package = importlib.import_module("tigrbl_identity_storage.migrations.versions")
        modules = [
            importlib.import_module(module.name)
            for module in pkgutil.iter_modules(
                versions_package.__path__, versions_package.__name__ + "."
            )
        ]
        before_adoption = [module for module in modules if module.revision != "0038_adopt_component_ownership"]
        adoption = next(module for module in modules if module.revision == "0038_adopt_component_ownership")
        for module in sorted(before_adoption, key=lambda value: value.revision):
            module.upgrade(connection)
        connection.exec_driver_sql(
            "INSERT INTO operator_metadata (key, value_json, updated_at) VALUES (?, ?, ?)",
            ("cutover-proof", '{"preserved":true}', "2026-08-05T00:00:00+00:00"),
        )
        monkeypatch.setattr(importlib.metadata, "version", lambda _distribution: "0.4.0.dev2")
        adoption.upgrade(connection)
        assert connection.exec_driver_sql(
            "SELECT value_json FROM operator_metadata WHERE key = 'cutover-proof'"
        ).scalar_one() == '{"preserved":true}'
        assert connection.exec_driver_sql(
            "SELECT COUNT(*) FROM tigrbl_schema_ownership"
        ).scalar_one() == 153
        assert connection.exec_driver_sql(
            "SELECT COUNT(*) FROM tigrbl_schema_migrations WHERE application_mode = 'adopted'"
        ).scalar_one() == 29
    finally:
        connection.close()
        engine.dispose()


def test_standalone_sources_do_not_import_the_compatibility_package() -> None:
    storage_root = Path(__file__).parents[2] / "pkgs/01-storage"
    for import_root in COMPONENT_IMPORT_ROOTS:
        distribution = import_root.replace("_", "-")
        source_root = storage_root / distribution / "src" / import_root
        for path in source_root.rglob("*.py"):
            text = path.read_text(encoding="utf-8")
            assert "tigrbl_identity_storage." not in text


def test_checked_in_deployment_lock_matches_every_manifest_digest() -> None:
    composition, _migrations, _models = _model_inventory()
    with as_file(files("tigrbl_identity_storage").joinpath("storage.lock.toml")) as path:
        lock = DeploymentLock.from_toml(path)
    lock.verify(
        composition,
        artifact_versions={manifest.component_id: "0.4.0.dev2" for manifest in composition.manifests},
    )


@pytest.mark.parametrize("import_root", COMPONENT_IMPORT_ROOTS)
def test_every_released_component_has_one_certified_head(import_root: str) -> None:
    component = importlib.import_module(import_root)
    composition, migrations = load_full_composition()
    graph = composition.graph(migrations)
    assert graph.component_heads(component.MANIFEST.component_id) == (
        component.MANIFEST.migration_head,
    )
