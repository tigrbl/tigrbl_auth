"""Initial owned schema for tigrbl.identity.storage.authorization-policy."""
from tigrbl_migrations import Migration
from tigrbl_identity_storage_authorization_policy.tables import TABLE_MODELS

REVISION = "0ef0b038-e979-5ba7-b874-d36093292702"

def upgrade(connection):
    for model in TABLE_MODELS:
        model.__table__.create(bind=connection, checkfirst=True)

def downgrade(connection):
    for model in reversed(TABLE_MODELS):
        model.__table__.drop(bind=connection, checkfirst=True)

MIGRATION = Migration(
    component="tigrbl.identity.storage.authorization-policy",
    revision=REVISION,
    parents=(),
    kind="standard",
    reversible=True,
    upgrade=upgrade,
    downgrade=downgrade,
)
