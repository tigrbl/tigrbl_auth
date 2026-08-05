"""Initial owned schema for tigrbl.identity.storage.workload-identity."""
from tigrbl_migrations import Migration
from tigrbl_identity_storage_workload_identity.tables import TABLE_MODELS

REVISION = "0bcee998-b0a3-5ba2-b04c-d049cad65127"

def upgrade(connection):
    for model in TABLE_MODELS:
        model.__table__.create(bind=connection, checkfirst=True)

def downgrade(connection):
    for model in reversed(TABLE_MODELS):
        model.__table__.drop(bind=connection, checkfirst=True)

MIGRATION = Migration(
    component="tigrbl.identity.storage.workload-identity",
    revision=REVISION,
    parents=(),
    kind="standard",
    reversible=True,
    upgrade=upgrade,
    downgrade=downgrade,
)
