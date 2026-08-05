"""Initial owned schema for tigrbl.identity.storage.consent."""
from tigrbl_migrations import Migration
from tigrbl_identity_storage_consent.tables import TABLE_MODELS

REVISION = "4541f213-14f7-544d-aec6-ac2302c8639e"

def upgrade(connection):
    for model in TABLE_MODELS:
        model.__table__.create(bind=connection, checkfirst=True)

def downgrade(connection):
    for model in reversed(TABLE_MODELS):
        model.__table__.drop(bind=connection, checkfirst=True)

MIGRATION = Migration(
    component="tigrbl.identity.storage.consent",
    revision=REVISION,
    parents=(),
    kind="standard",
    reversible=True,
    upgrade=upgrade,
    downgrade=downgrade,
)
