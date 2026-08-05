"""Initial owned schema for tigrbl.identity.storage.tenancy."""
from tigrbl_migrations import Migration
from tigrbl_identity_storage_tenancy.tables import TABLE_MODELS

REVISION = "69854e73-52d3-53ec-9542-6737159e42d6"

def upgrade(connection):
    for model in TABLE_MODELS:
        model.__table__.create(bind=connection, checkfirst=True)

def downgrade(connection):
    for model in reversed(TABLE_MODELS):
        model.__table__.drop(bind=connection, checkfirst=True)

MIGRATION = Migration(
    component="tigrbl.identity.storage.tenancy",
    revision=REVISION,
    parents=(),
    kind="standard",
    reversible=True,
    upgrade=upgrade,
    downgrade=downgrade,
)
