from __future__ import annotations

import importlib

from sqlalchemy import create_engine, inspect


MIGRATION = importlib.import_module(
    "tigrbl_identity_storage.migrations.versions.0023_artifact_and_token_profile_discriminators"
)


def _columns(conn, table: str) -> set[str]:
    return {column["name"] for column in inspect(conn).get_columns(table, schema="authn")}


def test_migration_0023_upgrades_downgrades_and_reapplies_on_sqlite() -> None:
    engine = create_engine("sqlite://")
    with engine.begin() as conn:
        conn.exec_driver_sql("ATTACH DATABASE ':memory:' AS authn")
        for table in MIGRATION.GROUPS:
            conn.exec_driver_sql(f"CREATE TABLE authn.{table} (id VARCHAR(36) PRIMARY KEY)")
        MIGRATION.upgrade(conn)
        for table, columns in MIGRATION.GROUPS.items():
            assert {name for name, _ in columns} <= _columns(conn, table)
        MIGRATION.downgrade(conn)
        for table, columns in MIGRATION.GROUPS.items():
            assert not ({name for name, _ in columns} & _columns(conn, table))
        MIGRATION.upgrade(conn)
        for table, columns in MIGRATION.GROUPS.items():
            assert {name for name, _ in columns} <= _columns(conn, table)
