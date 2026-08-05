"""Initial owned schema for tigrbl.identity.storage.token."""
from tigrbl_migrations import Migration
from tigrbl_identity_storage_token.tables import TABLE_MODELS

REVISION = "563f6816-43af-5ca0-8c78-b73eec393c1c"

def upgrade(connection):
    for model in TABLE_MODELS:
        model.__table__.create(bind=connection, checkfirst=True)

def downgrade(connection):
    for model in reversed(TABLE_MODELS):
        model.__table__.drop(bind=connection, checkfirst=True)

MIGRATION = Migration(
    component="tigrbl.identity.storage.token",
    revision=REVISION,
    parents=(),
    kind="standard",
    reversible=True,
    upgrade=upgrade,
    downgrade=downgrade,
)
