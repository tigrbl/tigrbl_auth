import importlib

from sqlalchemy import create_engine, inspect

migration = importlib.import_module(
    "tigrbl_identity_storage.migrations.versions.0033_replay_reservations"
)


def test_0033_upgrade_downgrade_reapply():
    engine = create_engine("sqlite:///:memory:")
    with engine.begin() as conn:
        conn.exec_driver_sql("ATTACH DATABASE ':memory:' AS authn")
        migration.upgrade(conn)
        assert "replay_reservations" in inspect(conn).get_table_names(schema="authn")
        migration.downgrade(conn)
        assert "replay_reservations" not in inspect(conn).get_table_names(schema="authn")
        migration.upgrade(conn)
        assert "replay_reservations" in inspect(conn).get_table_names(schema="authn")
