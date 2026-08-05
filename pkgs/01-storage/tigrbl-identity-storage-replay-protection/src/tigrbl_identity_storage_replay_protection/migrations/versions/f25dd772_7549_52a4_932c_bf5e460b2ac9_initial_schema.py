"""Initial owned schema for tigrbl.identity.storage.replay-protection."""
from tigrbl_migrations import Migration
from tigrbl_identity_storage_replay_protection.tables import TABLE_MODELS

REVISION = "f25dd772-7549-52a4-932c-bf5e460b2ac9"

def upgrade(connection):
    for model in TABLE_MODELS:
        model.__table__.create(bind=connection, checkfirst=True)

def downgrade(connection):
    for model in reversed(TABLE_MODELS):
        model.__table__.drop(bind=connection, checkfirst=True)

MIGRATION = Migration(
    component="tigrbl.identity.storage.replay-protection",
    revision=REVISION,
    parents=(),
    kind="standard",
    reversible=True,
    upgrade=upgrade,
    downgrade=downgrade,
)
