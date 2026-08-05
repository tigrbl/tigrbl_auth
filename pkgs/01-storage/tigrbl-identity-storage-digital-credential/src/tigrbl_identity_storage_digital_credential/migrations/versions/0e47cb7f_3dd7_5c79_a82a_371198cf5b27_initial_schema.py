"""Initial owned schema for tigrbl.identity.storage.digital-credential."""
from tigrbl_migrations import Migration
from tigrbl_identity_storage_digital_credential.tables import TABLE_MODELS

REVISION = "0e47cb7f-3dd7-5c79-a82a-371198cf5b27"

def upgrade(connection):
    for model in TABLE_MODELS:
        model.__table__.create(bind=connection, checkfirst=True)

def downgrade(connection):
    for model in reversed(TABLE_MODELS):
        model.__table__.drop(bind=connection, checkfirst=True)

MIGRATION = Migration(
    component="tigrbl.identity.storage.digital-credential",
    revision=REVISION,
    parents=(),
    kind="standard",
    reversible=True,
    upgrade=upgrade,
    downgrade=downgrade,
)
