"""Initial owned schema for tigrbl.identity.storage.federation."""
from tigrbl_migrations import Migration
from tigrbl_identity_storage_federation.tables import TABLE_MODELS

REVISION = "d0a7da98-00a5-58f8-ac3e-d0912c96f0db"

def upgrade(connection):
    for model in TABLE_MODELS:
        model.__table__.create(bind=connection, checkfirst=True)

def downgrade(connection):
    for model in reversed(TABLE_MODELS):
        model.__table__.drop(bind=connection, checkfirst=True)

MIGRATION = Migration(
    component="tigrbl.identity.storage.federation",
    revision=REVISION,
    parents=(),
    kind="standard",
    reversible=True,
    upgrade=upgrade,
    downgrade=downgrade,
)
