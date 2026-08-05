"""Initial owned schema for tigrbl.identity.storage.release-governance."""
from tigrbl_migrations import Migration
from tigrbl_identity_storage_release_governance.tables import TABLE_MODELS

REVISION = "90c6e0ac-6f27-5837-9d8b-895adb4679d5"

def upgrade(connection):
    for model in TABLE_MODELS:
        model.__table__.create(bind=connection, checkfirst=True)

def downgrade(connection):
    for model in reversed(TABLE_MODELS):
        model.__table__.drop(bind=connection, checkfirst=True)

MIGRATION = Migration(
    component="tigrbl.identity.storage.release-governance",
    revision=REVISION,
    parents=(),
    kind="standard",
    reversible=True,
    upgrade=upgrade,
    downgrade=downgrade,
)
