"""Initial owned schema for tigrbl.identity.storage.attestation."""
from tigrbl_migrations import Migration
from tigrbl_identity_storage_attestation.tables import TABLE_MODELS

REVISION = "7e916983-3ad7-51a7-bf4a-79ce229eb092"

def upgrade(connection):
    for model in TABLE_MODELS:
        model.__table__.create(bind=connection, checkfirst=True)

def downgrade(connection):
    for model in reversed(TABLE_MODELS):
        model.__table__.drop(bind=connection, checkfirst=True)

MIGRATION = Migration(
    component="tigrbl.identity.storage.attestation",
    revision=REVISION,
    parents=(),
    kind="standard",
    reversible=True,
    upgrade=upgrade,
    downgrade=downgrade,
)
