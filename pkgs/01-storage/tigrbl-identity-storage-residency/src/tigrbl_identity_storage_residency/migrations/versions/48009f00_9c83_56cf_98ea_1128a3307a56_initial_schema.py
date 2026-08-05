"""Initial owned schema for tigrbl.identity.storage.residency."""
from tigrbl_migrations import Migration
from tigrbl_identity_storage_residency.tables import TABLE_MODELS

REVISION = "48009f00-9c83-56cf-98ea-1128a3307a56"

def upgrade(connection):
    for model in TABLE_MODELS:
        model.__table__.create(bind=connection, checkfirst=True)

def downgrade(connection):
    for model in reversed(TABLE_MODELS):
        model.__table__.drop(bind=connection, checkfirst=True)

MIGRATION = Migration(
    component="tigrbl.identity.storage.residency",
    revision=REVISION,
    parents=(),
    kind="standard",
    reversible=True,
    upgrade=upgrade,
    downgrade=downgrade,
)
