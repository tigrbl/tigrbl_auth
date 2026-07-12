from __future__ import annotations
import importlib
from sqlalchemy import create_engine, inspect

MIGRATION = importlib.import_module(
    "tigrbl_identity_storage.migrations.versions.0025_credential_issuance_and_status"
)


def _names(conn):
    return set(inspect(conn).get_table_names(schema="authn"))


def test_migration_0025_upgrades_downgrades_and_reapplies_on_sqlite():
    with create_engine("sqlite://").begin() as conn:
        conn.exec_driver_sql("ATTACH DATABASE ':memory:' AS authn")
        expected = {table.__tablename__ for table in MIGRATION.TABLES}
        MIGRATION.upgrade(conn)
        assert expected <= _names(conn)
        MIGRATION.downgrade(conn)
        assert not expected & _names(conn)
        MIGRATION.upgrade(conn)
        assert expected <= _names(conn)
