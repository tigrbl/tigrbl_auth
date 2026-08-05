"""Initial owned schema for tigrbl.identity.storage.operator."""
from tigrbl_migrations import Migration
from tigrbl_identity_storage_operator.tables import TABLE_MODELS

REVISION = "469839b2-d339-544a-b747-fd68b6a5f235"

def upgrade(connection):
    for model in TABLE_MODELS:
        model.__table__.create(bind=connection, checkfirst=True)

def downgrade(connection):
    for model in reversed(TABLE_MODELS):
        model.__table__.drop(bind=connection, checkfirst=True)

MIGRATION = Migration(
    component="tigrbl.identity.storage.operator",
    revision=REVISION,
    parents=(),
    kind="standard",
    reversible=True,
    upgrade=upgrade,
    downgrade=downgrade,
)
