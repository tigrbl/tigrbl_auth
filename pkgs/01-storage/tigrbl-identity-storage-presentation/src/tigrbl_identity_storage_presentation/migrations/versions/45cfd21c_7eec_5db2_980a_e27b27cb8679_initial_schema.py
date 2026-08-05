"""Initial owned schema for tigrbl.identity.storage.presentation."""
from tigrbl_migrations import Migration
from tigrbl_identity_storage_presentation.tables import TABLE_MODELS

REVISION = "45cfd21c-7eec-5db2-980a-e27b27cb8679"

def upgrade(connection):
    for model in TABLE_MODELS:
        model.__table__.create(bind=connection, checkfirst=True)

def downgrade(connection):
    for model in reversed(TABLE_MODELS):
        model.__table__.drop(bind=connection, checkfirst=True)

MIGRATION = Migration(
    component="tigrbl.identity.storage.presentation",
    revision=REVISION,
    parents=(),
    kind="standard",
    reversible=True,
    upgrade=upgrade,
    downgrade=downgrade,
)
