"""Initial owned schema for tigrbl.identity.storage.webauthn."""
from tigrbl_migrations import Migration
from tigrbl_identity_storage_webauthn.tables import TABLE_MODELS

REVISION = "35709893-1208-54c2-ab00-dca4b2e67065"

def upgrade(connection):
    for model in TABLE_MODELS:
        model.__table__.create(bind=connection, checkfirst=True)

def downgrade(connection):
    for model in reversed(TABLE_MODELS):
        model.__table__.drop(bind=connection, checkfirst=True)

MIGRATION = Migration(
    component="tigrbl.identity.storage.webauthn",
    revision=REVISION,
    parents=(),
    kind="standard",
    reversible=True,
    upgrade=upgrade,
    downgrade=downgrade,
)
