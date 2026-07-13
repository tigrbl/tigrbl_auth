import importlib

from sqlalchemy import create_engine, inspect

MIGRATION = importlib.import_module(
    "tigrbl_identity_storage.migrations.versions.0032_claim_definition_and_provenance"
)


def names(conn):
    return set(inspect(conn).get_table_names(schema="authn"))


def test_0032_upgrade_downgrade_reapply():
    with create_engine("sqlite://").begin() as conn:
        conn.exec_driver_sql("ATTACH DATABASE ':memory:' AS authn")
        expected = {table.__tablename__ for table in MIGRATION.TABLES}
        MIGRATION.upgrade(conn)
        assert expected <= names(conn)
        MIGRATION.downgrade(conn)
        assert not expected & names(conn)
        MIGRATION.upgrade(conn)
        assert expected <= names(conn)
