"""Initial owned schema for tigrbl.identity.storage.trust-federation-graph."""
from tigrbl_migrations import Migration
from tigrbl_identity_storage_trust_federation_graph.tables import TABLE_MODELS

REVISION = "88f90844-5618-5007-9883-d1d6f7c35d66"

def upgrade(connection):
    for model in TABLE_MODELS:
        model.__table__.create(bind=connection, checkfirst=True)

def downgrade(connection):
    for model in reversed(TABLE_MODELS):
        model.__table__.drop(bind=connection, checkfirst=True)

MIGRATION = Migration(
    component="tigrbl.identity.storage.trust-federation-graph",
    revision=REVISION,
    parents=(),
    kind="standard",
    reversible=True,
    upgrade=upgrade,
    downgrade=downgrade,
)
