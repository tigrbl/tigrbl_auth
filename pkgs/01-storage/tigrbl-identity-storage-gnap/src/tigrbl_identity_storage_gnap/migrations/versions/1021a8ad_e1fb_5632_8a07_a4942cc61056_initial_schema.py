"""Initial owned schema for tigrbl.identity.storage.gnap."""
from tigrbl_migrations import Migration
from tigrbl_identity_storage_gnap.tables import TABLE_MODELS

REVISION = "1021a8ad-e1fb-5632-8a07-a4942cc61056"

def upgrade(connection):
    for model in TABLE_MODELS:
        model.__table__.create(bind=connection, checkfirst=True)

def downgrade(connection):
    for model in reversed(TABLE_MODELS):
        model.__table__.drop(bind=connection, checkfirst=True)

MIGRATION = Migration(
    component="tigrbl.identity.storage.gnap",
    revision=REVISION,
    parents=(),
    kind="standard",
    reversible=True,
    upgrade=upgrade,
    downgrade=downgrade,
)
