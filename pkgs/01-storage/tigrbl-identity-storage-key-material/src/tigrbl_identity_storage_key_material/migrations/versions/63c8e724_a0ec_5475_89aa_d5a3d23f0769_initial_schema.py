"""Initial owned schema for tigrbl.identity.storage.key-material."""
from tigrbl_migrations import Migration
from tigrbl_identity_storage_key_material.tables import TABLE_MODELS

REVISION = "63c8e724-a0ec-5475-89aa-d5a3d23f0769"

def upgrade(connection):
    for model in TABLE_MODELS:
        model.__table__.create(bind=connection, checkfirst=True)

def downgrade(connection):
    for model in reversed(TABLE_MODELS):
        model.__table__.drop(bind=connection, checkfirst=True)

MIGRATION = Migration(
    component="tigrbl.identity.storage.key-material",
    revision=REVISION,
    parents=(),
    kind="standard",
    reversible=True,
    upgrade=upgrade,
    downgrade=downgrade,
)
