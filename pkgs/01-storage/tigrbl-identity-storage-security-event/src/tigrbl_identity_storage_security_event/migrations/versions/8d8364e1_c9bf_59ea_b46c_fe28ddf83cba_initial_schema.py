"""Initial owned schema for tigrbl.identity.storage.security-event."""
from tigrbl_migrations import Migration
from tigrbl_identity_storage_security_event.tables import TABLE_MODELS

REVISION = "8d8364e1-c9bf-59ea-b46c-fe28ddf83cba"

def upgrade(connection):
    for model in TABLE_MODELS:
        model.__table__.create(bind=connection, checkfirst=True)

def downgrade(connection):
    for model in reversed(TABLE_MODELS):
        model.__table__.drop(bind=connection, checkfirst=True)

MIGRATION = Migration(
    component="tigrbl.identity.storage.security-event",
    revision=REVISION,
    parents=(),
    kind="standard",
    reversible=True,
    upgrade=upgrade,
    downgrade=downgrade,
)
