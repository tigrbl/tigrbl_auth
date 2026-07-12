from __future__ import annotations
import importlib
from sqlalchemy import create_engine, inspect

MIGRATION = importlib.import_module(
    "tigrbl_identity_storage.migrations.versions.0024_credential_issuer_wallet_and_configuration"
)


def _names(conn):
    return set(inspect(conn).get_table_names(schema="authn"))


def test_migration_0024_upgrades_downgrades_and_reapplies_on_sqlite():
    engine = create_engine("sqlite://")
    with engine.begin() as conn:
        conn.exec_driver_sql("ATTACH DATABASE ':memory:' AS authn")
        expected = {table.__tablename__ for table in MIGRATION.TABLES}
        MIGRATION.upgrade(conn)
        assert expected <= _names(conn)
        MIGRATION.downgrade(conn)
        assert not expected & _names(conn)
        MIGRATION.upgrade(conn)
        assert expected <= _names(conn)
