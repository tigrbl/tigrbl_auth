"""Initial owned schema for tigrbl.identity.storage.scim."""
from tigrbl_migrations import Migration
from tigrbl_identity_storage_scim.tables import TABLE_MODELS

REVISION = "6bf4ad16-462a-5913-9322-f1ccbf2a82f5"

def upgrade(connection):
    for model in TABLE_MODELS:
        model.__table__.create(bind=connection, checkfirst=True)

def downgrade(connection):
    for model in reversed(TABLE_MODELS):
        model.__table__.drop(bind=connection, checkfirst=True)

MIGRATION = Migration(
    component="tigrbl.identity.storage.scim",
    revision=REVISION,
    parents=(),
    kind="standard",
    reversible=True,
    upgrade=upgrade,
    downgrade=downgrade,
)
