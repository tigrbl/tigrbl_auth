"""Initial owned schema for tigrbl.identity.storage.certificate."""
from tigrbl_migrations import Migration
from tigrbl_identity_storage_certificate.tables import TABLE_MODELS

REVISION = "a7e704e3-722e-5a59-92a6-9825004d8817"

def upgrade(connection):
    for model in TABLE_MODELS:
        model.__table__.create(bind=connection, checkfirst=True)

def downgrade(connection):
    for model in reversed(TABLE_MODELS):
        model.__table__.drop(bind=connection, checkfirst=True)

MIGRATION = Migration(
    component="tigrbl.identity.storage.certificate",
    revision=REVISION,
    parents=(),
    kind="standard",
    reversible=True,
    upgrade=upgrade,
    downgrade=downgrade,
)
