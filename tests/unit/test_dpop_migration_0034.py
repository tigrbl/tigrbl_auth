import importlib

from sqlalchemy import create_engine, inspect

migration = importlib.import_module(
    "tigrbl_identity_storage.migrations.versions.0034_dpop_replay_nonce_tables"
)


def test_0034_upgrade_downgrade_reapply() -> None:
    engine = create_engine("sqlite:///:memory:")
    with engine.begin() as conn:
        conn.exec_driver_sql("ATTACH DATABASE ':memory:' AS authn")
        migration.upgrade(conn)
        assert set(inspect(conn).get_table_names(schema="authn")).issuperset(
            {"dpop_replays", "dpop_nonces"}
        )
        migration.downgrade(conn)
        assert set(inspect(conn).get_table_names(schema="authn")).isdisjoint(
            {"dpop_replays", "dpop_nonces"}
        )
        migration.upgrade(conn)
        assert set(inspect(conn).get_table_names(schema="authn")).issuperset(
            {"dpop_replays", "dpop_nonces"}
        )
