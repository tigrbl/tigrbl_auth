"""Adopt the frozen monolithic schema into component-owned migration ledgers."""

from __future__ import annotations

import importlib
import importlib.metadata

from sqlalchemy import inspect

from tigrbl_identity_storage.components import load_full_composition
from tigrbl_migrations import MigrationLedger

revision = "0038_adopt_component_ownership"
down_revision = "0037_operator_tables"
branch_labels = None
depends_on = None


def _verify_owned_tables(conn, composition) -> None:
    inspector = inspect(conn)
    for manifest in composition.manifests:
        for owned in manifest.objects:
            if owned.kind != "table" or owned.model is None:
                continue
            if "." in owned.physical_name:
                schema, table_name = owned.physical_name.split(".", 1)
            else:
                schema, table_name = None, owned.physical_name
            if table_name not in set(inspector.get_table_names(schema=schema)):
                raise RuntimeError(f"cannot adopt missing table {owned.physical_name}")
            module_name, attribute = owned.model.split(":", 1)
            model = getattr(importlib.import_module(module_name), attribute)
            expected = {column.name for column in model.__table__.columns}
            actual = {column["name"] for column in inspector.get_columns(table_name, schema=schema)}
            if expected != actual:
                raise RuntimeError(
                    f"cannot adopt structurally different table {owned.physical_name}: "
                    f"expected columns {sorted(expected)}, found {sorted(actual)}"
                )


def upgrade(conn) -> None:
    composition, migrations = load_full_composition()
    _verify_owned_tables(conn, composition)
    by_revision = {migration.revision: migration for migration in migrations}
    ledger = MigrationLedger(conn)
    ledger.bootstrap()
    execution_id = ledger.acquire_lock()
    try:
        for manifest in composition.manifests:
            artifact_version = importlib.metadata.version(manifest.distribution)
            migration = by_revision[manifest.migration_head]
            ledger.record_migration(
                migration,
                artifact_version=artifact_version,
                execution_id=execution_id,
                application_mode="adopted",
            )
            ledger.claim_objects(manifest, revision=migration.revision)
            ledger.record_component(manifest, artifact_version=artifact_version)
    finally:
        ledger.release_lock(execution_id)


def downgrade(conn) -> None:
    raise RuntimeError("component ownership adoption is forward-only")
