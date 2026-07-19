import importlib
from sqlalchemy import create_engine, inspect
from tigrbl_identity_storage.tables import SvidRecord
migration=importlib.import_module("tigrbl_identity_storage.migrations.versions.0036_workload_credentials_artifacts_and_proof_replay")

def test_0036_upgrade_downgrade_reapply()->None:
    engine=create_engine("sqlite:///:memory:")
    with engine.begin() as conn:
        conn.exec_driver_sql("ATTACH DATABASE ':memory:' AS authn")
        SvidRecord.__table__.create(conn)
        migration.upgrade(conn)
        tables=set(inspect(conn).get_table_names(schema="authn"))
        assert {"workload_reference_bindings","workload_credential_entitlements","protected_artifact_references","possession_proof_replays"}.issubset(tables)
        columns={column["name"] for column in inspect(conn).get_columns("svid_records",schema="authn")}
        assert {"proof_key_id","confirmation_key_thumbprint","profile_revision"}.issubset(columns)
        migration.downgrade(conn)
        migration.upgrade(conn)
        assert "possession_proof_replays" in inspect(conn).get_table_names(schema="authn")

def test_0036_extends_current_head()->None:
    assert migration.down_revision=="0035_webauthn_rp_ceremony_and_credentials"