import importlib
from sqlalchemy import create_engine, inspect

MIGRATION = importlib.import_module(
    "tigrbl_identity_storage.migrations.versions.0030_optional_did_and_gnap_state"
)


def names(conn):
    return set(inspect(conn).get_table_names(schema="authn"))


def test_0030_upgrade_downgrade_reapply():
    with create_engine("sqlite://").begin() as conn:
        conn.exec_driver_sql("ATTACH DATABASE ':memory:' AS authn")
        expected = {t.__tablename__ for t in MIGRATION.TABLES}
        MIGRATION.upgrade(conn)
        assert expected <= names(conn)
        MIGRATION.downgrade(conn)
        assert not expected & names(conn)
        MIGRATION.upgrade(conn)
        assert expected <= names(conn)
