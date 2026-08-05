"""Initial owned schema for tigrbl.identity.storage.principals."""
from tigrbl_migrations import Migration
from tigrbl_identity_storage_principals.tables import TABLE_MODELS

REVISION = "44ff280d-bf80-54b1-9bb2-c796f258bd4d"

def upgrade(connection):
    for model in TABLE_MODELS:
        model.__table__.create(bind=connection, checkfirst=True)

def downgrade(connection):
    for model in reversed(TABLE_MODELS):
        model.__table__.drop(bind=connection, checkfirst=True)

MIGRATION = Migration(
    component="tigrbl.identity.storage.principals",
    revision=REVISION,
    parents=(),
    kind="standard",
    reversible=True,
    upgrade=upgrade,
    downgrade=downgrade,
)
