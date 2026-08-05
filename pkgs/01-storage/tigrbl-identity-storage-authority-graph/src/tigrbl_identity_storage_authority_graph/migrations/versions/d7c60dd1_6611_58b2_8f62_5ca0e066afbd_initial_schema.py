"""Initial owned schema for tigrbl.identity.storage.authority-graph."""
from tigrbl_migrations import Migration
from tigrbl_identity_storage_authority_graph.tables import TABLE_MODELS

REVISION = "d7c60dd1-6611-58b2-8f62-5ca0e066afbd"

def upgrade(connection):
    for model in TABLE_MODELS:
        model.__table__.create(bind=connection, checkfirst=True)

def downgrade(connection):
    for model in reversed(TABLE_MODELS):
        model.__table__.drop(bind=connection, checkfirst=True)

MIGRATION = Migration(
    component="tigrbl.identity.storage.authority-graph",
    revision=REVISION,
    parents=(),
    kind="standard",
    reversible=True,
    upgrade=upgrade,
    downgrade=downgrade,
)
