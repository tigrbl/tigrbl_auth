"""Initial owned schema for tigrbl.identity.storage.oidc."""
from tigrbl_migrations import Migration
from tigrbl_identity_storage_oidc.tables import TABLE_MODELS

REVISION = "d33404e7-316b-5c4e-8336-5103efa79186"

def upgrade(connection):
    for model in TABLE_MODELS:
        model.__table__.create(bind=connection, checkfirst=True)

def downgrade(connection):
    for model in reversed(TABLE_MODELS):
        model.__table__.drop(bind=connection, checkfirst=True)

MIGRATION = Migration(
    component="tigrbl.identity.storage.oidc",
    revision=REVISION,
    parents=(),
    kind="standard",
    reversible=True,
    upgrade=upgrade,
    downgrade=downgrade,
)
