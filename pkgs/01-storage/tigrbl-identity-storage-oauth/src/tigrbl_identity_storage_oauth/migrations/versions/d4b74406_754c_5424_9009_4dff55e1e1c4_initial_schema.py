"""Initial owned schema for tigrbl.identity.storage.oauth."""
from tigrbl_migrations import Migration
from tigrbl_identity_storage_oauth.tables import TABLE_MODELS

REVISION = "d4b74406-754c-5424-9009-4dff55e1e1c4"

def upgrade(connection):
    for model in TABLE_MODELS:
        model.__table__.create(bind=connection, checkfirst=True)

def downgrade(connection):
    for model in reversed(TABLE_MODELS):
        model.__table__.drop(bind=connection, checkfirst=True)

MIGRATION = Migration(
    component="tigrbl.identity.storage.oauth",
    revision=REVISION,
    parents=(),
    kind="standard",
    reversible=True,
    upgrade=upgrade,
    downgrade=downgrade,
)
