"""Initial owned schema for tigrbl.identity.storage.access-governance."""
from tigrbl_migrations import Migration
from tigrbl_identity_storage_access_governance.tables import TABLE_MODELS

REVISION = "851b516f-e2a5-533b-8a68-a9ac3f9c7cb5"

def upgrade(connection):
    for model in TABLE_MODELS:
        model.__table__.create(bind=connection, checkfirst=True)

def downgrade(connection):
    for model in reversed(TABLE_MODELS):
        model.__table__.drop(bind=connection, checkfirst=True)

MIGRATION = Migration(
    component="tigrbl.identity.storage.access-governance",
    revision=REVISION,
    parents=(),
    kind="standard",
    reversible=True,
    upgrade=upgrade,
    downgrade=downgrade,
)
