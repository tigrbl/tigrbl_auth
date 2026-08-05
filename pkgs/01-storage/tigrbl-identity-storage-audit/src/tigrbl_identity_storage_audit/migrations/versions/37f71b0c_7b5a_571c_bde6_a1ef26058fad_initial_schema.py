"""Initial owned schema for tigrbl.identity.storage.audit."""
from tigrbl_migrations import Migration
from tigrbl_identity_storage_audit.tables import TABLE_MODELS

REVISION = "37f71b0c-7b5a-571c-bde6-a1ef26058fad"

def upgrade(connection):
    for model in TABLE_MODELS:
        model.__table__.create(bind=connection, checkfirst=True)

def downgrade(connection):
    for model in reversed(TABLE_MODELS):
        model.__table__.drop(bind=connection, checkfirst=True)

MIGRATION = Migration(
    component="tigrbl.identity.storage.audit",
    revision=REVISION,
    parents=(),
    kind="standard",
    reversible=True,
    upgrade=upgrade,
    downgrade=downgrade,
)
