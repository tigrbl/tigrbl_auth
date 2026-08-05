"""Initial owned schema for tigrbl.identity.storage.authentication."""
from tigrbl_migrations import Migration
from tigrbl_identity_storage_authentication.tables import TABLE_MODELS

REVISION = "79c73e01-df92-5166-844d-b2e96bcae30b"

def upgrade(connection):
    for model in TABLE_MODELS:
        model.__table__.create(bind=connection, checkfirst=True)

def downgrade(connection):
    for model in reversed(TABLE_MODELS):
        model.__table__.drop(bind=connection, checkfirst=True)

MIGRATION = Migration(
    component="tigrbl.identity.storage.authentication",
    revision=REVISION,
    parents=(),
    kind="standard",
    reversible=True,
    upgrade=upgrade,
    downgrade=downgrade,
)
