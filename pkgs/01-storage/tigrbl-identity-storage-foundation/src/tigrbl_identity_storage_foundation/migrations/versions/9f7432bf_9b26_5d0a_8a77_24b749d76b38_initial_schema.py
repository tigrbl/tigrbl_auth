"""Initial owned schema for tigrbl.identity.storage.foundation."""
from tigrbl_migrations import Migration
from tigrbl_identity_storage_foundation.tables import TABLE_MODELS

REVISION = "9f7432bf-9b26-5d0a-8a77-24b749d76b38"

def upgrade(connection):
    for model in TABLE_MODELS:
        model.__table__.create(bind=connection, checkfirst=True)

def downgrade(connection):
    for model in reversed(TABLE_MODELS):
        model.__table__.drop(bind=connection, checkfirst=True)

MIGRATION = Migration(
    component="tigrbl.identity.storage.foundation",
    revision=REVISION,
    parents=(),
    kind="standard",
    reversible=True,
    upgrade=upgrade,
    downgrade=downgrade,
)
