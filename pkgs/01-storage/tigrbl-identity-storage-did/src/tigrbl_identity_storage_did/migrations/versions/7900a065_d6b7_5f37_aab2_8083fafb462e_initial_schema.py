"""Initial owned schema for tigrbl.identity.storage.did."""
from tigrbl_migrations import Migration
from tigrbl_identity_storage_did.tables import TABLE_MODELS

REVISION = "7900a065-d6b7-5f37-aab2-8083fafb462e"

def upgrade(connection):
    for model in TABLE_MODELS:
        model.__table__.create(bind=connection, checkfirst=True)

def downgrade(connection):
    for model in reversed(TABLE_MODELS):
        model.__table__.drop(bind=connection, checkfirst=True)

MIGRATION = Migration(
    component="tigrbl.identity.storage.did",
    revision=REVISION,
    parents=(),
    kind="standard",
    reversible=True,
    upgrade=upgrade,
    downgrade=downgrade,
)
