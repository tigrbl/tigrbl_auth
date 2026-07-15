import importlib

from sqlalchemy import create_engine, inspect

from tigrbl_identity_storage.tables import CredentialWebAuthnPasskey

migration = importlib.import_module(
    "tigrbl_identity_storage.migrations.versions.0035_webauthn_rp_ceremony_and_credentials"
)


def test_0035_upgrade_downgrade_reapply() -> None:
    engine = create_engine("sqlite:///:memory:")
    with engine.begin() as conn:
        conn.exec_driver_sql("ATTACH DATABASE ':memory:' AS authn")
        CredentialWebAuthnPasskey.__table__.create(conn)
        migration.upgrade(conn)
        tables = set(inspect(conn).get_table_names(schema="authn"))
        assert tables.issuperset(
            {
                "webauthn_ceremonies",
                "webauthn_relying_parties",
                "webauthn_attestation_records",
            }
        )
        columns = {
            column["name"]
            for column in inspect(conn).get_columns(
                "credential_webauthn_passkeys", schema="authn"
            )
        }
        assert {
            "credential_external_id",
            "credential_public_key_cose",
            "backup_state",
        }.issubset(columns)
        migration.downgrade(conn)
        migration.upgrade(conn)
        assert "webauthn_ceremonies" in inspect(conn).get_table_names(schema="authn")


def test_0035_extends_current_migration_head() -> None:
    assert migration.down_revision == "0034_dpop_replay_nonce_tables"
