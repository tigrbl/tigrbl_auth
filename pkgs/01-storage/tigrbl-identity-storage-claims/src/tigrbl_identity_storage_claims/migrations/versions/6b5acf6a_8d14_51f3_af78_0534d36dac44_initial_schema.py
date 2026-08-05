"""Initial owned schema for tigrbl.identity.storage.claims."""
from tigrbl_migrations import Migration
from tigrbl_identity_storage_claims.tables import TABLE_MODELS

REVISION = "6b5acf6a-8d14-51f3-af78-0534d36dac44"

def upgrade(connection):
    for model in TABLE_MODELS:
        model.__table__.create(bind=connection, checkfirst=True)

def downgrade(connection):
    for model in reversed(TABLE_MODELS):
        model.__table__.drop(bind=connection, checkfirst=True)

MIGRATION = Migration(
    component="tigrbl.identity.storage.claims",
    revision=REVISION,
    parents=(),
    kind="standard",
    reversible=True,
    upgrade=upgrade,
    downgrade=downgrade,
)
