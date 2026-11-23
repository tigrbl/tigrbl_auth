"""Replace legacy API and service key verifiers with PBKDF2 verifiers."""

from tba_primitives_identity.credential_digests import (
    CREDENTIAL_DIGEST_V2_PREFIX,
    harden_legacy_credential_digest,
)
from tba_storage_authentication.tables import CredentialApiKey, CredentialServiceKey
from tigrbl_migrations import Migration

REVISION = "f52f17d5-c59d-4901-974b-64f3c1c19221"


def upgrade(connection):
    for model in (CredentialApiKey, CredentialServiceKey):
        table = model.__table__
        pending = (
            table.select()
            .with_only_columns(table.c.id, table.c.digest)
            .where(table.c.digest.not_like(f"{CREDENTIAL_DIGEST_V2_PREFIX}%"))
            .order_by(table.c.id)
            .limit(64)
        )
        while batch := connection.execute(pending).all():
            for row_id, digest in batch:
                connection.execute(
                    table.update()
                    .where(table.c.id == row_id, table.c.digest == digest)
                    .values(digest=harden_legacy_credential_digest(digest))
                )


MIGRATION = Migration(
    component="tigrbl.identity.storage.authentication",
    revision=REVISION,
    parents=("79c73e01-df92-5166-844d-b2e96bcae30b",),
    upgrade=upgrade,
)
