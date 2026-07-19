"""Add workload references, credential entitlements, artifact locators, and proof replay."""
from __future__ import annotations
from tigrbl_identity_storage.migrations.helpers import AUTHN_SCHEMA, column_names, create_tables, drop_columns, drop_tables
from tigrbl_identity_storage.tables import PossessionProofReplay, ProtectedArtifactReference, SvidRecord, WorkloadCredentialEntitlement, WorkloadReferenceBinding

revision="0036_workload_credentials_artifacts_and_proof_replay"
down_revision="0035_webauthn_rp_ceremony_and_credentials"
branch_labels=None
depends_on=None
NEW_TABLES=(WorkloadReferenceBinding,WorkloadCredentialEntitlement,ProtectedArtifactReference,PossessionProofReplay)
SVID_COLUMNS=(
    ("proof_key_id","proof_key_id VARCHAR(255)"),
    ("confirmation_key_thumbprint","confirmation_key_thumbprint VARCHAR(255)"),
    ("profile_revision","profile_revision VARCHAR(255)"),
)

def _table(name:str)->str: return f'"{AUTHN_SCHEMA}"."{name}"'

def upgrade(conn)->None:
    create_tables(conn,*NEW_TABLES)
    existing=column_names(conn,SvidRecord.__tablename__)
    for name,ddl in SVID_COLUMNS:
        if name not in existing: conn.exec_driver_sql(f"ALTER TABLE {_table(SvidRecord.__tablename__)} ADD COLUMN {ddl}")

def downgrade(conn)->None:
    drop_columns(conn,SvidRecord.__tablename__,[name for name,_ in SVID_COLUMNS])
    drop_tables(conn,*NEW_TABLES)