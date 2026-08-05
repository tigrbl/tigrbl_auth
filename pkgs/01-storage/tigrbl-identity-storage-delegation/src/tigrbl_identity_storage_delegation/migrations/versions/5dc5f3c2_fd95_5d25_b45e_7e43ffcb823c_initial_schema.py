"""Initial owned schema for tigrbl.identity.storage.delegation."""
from tigrbl_migrations import Migration
from tigrbl_identity_storage_delegation.tables import TABLE_MODELS

REVISION = "5dc5f3c2-fd95-5d25-b45e-7e43ffcb823c"

def upgrade(connection):
    for model in TABLE_MODELS:
        model.__table__.create(bind=connection, checkfirst=True)

def downgrade(connection):
    for model in reversed(TABLE_MODELS):
        model.__table__.drop(bind=connection, checkfirst=True)

MIGRATION = Migration(
    component="tigrbl.identity.storage.delegation",
    revision=REVISION,
    parents=(),
    kind="standard",
    reversible=True,
    upgrade=upgrade,
    downgrade=downgrade,
)
