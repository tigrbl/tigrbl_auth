"""Paired raw key issuance and verifier storage shared by credential tables."""

from __future__ import annotations

from secrets import token_urlsafe

from tigrbl._spec.io_spec import Pair
from tba_primitives_identity.credential_digests import (
    CREDENTIAL_DIGEST_LENGTH,
    credential_digest,
)
from tba_primitives_identity.orm import F, IO, S, KeyDigest, Mapped, String, acol


def _generate_pair(_context: dict | None = None) -> Pair:
    raw = token_urlsafe(32)
    return Pair(raw=raw, stored=credential_digest(raw))


class CredentialKeyDigest(KeyDigest):
    digest: Mapped[str] = acol(
        storage=S(String, nullable=False, unique=True, index=True),
        field=F(constraints={"max_length": CREDENTIAL_DIGEST_LENGTH}),
        io=IO(out_verbs=("read", "list", "create")).paired(
            make=_generate_pair,
            alias="api_key",
            verbs=("create",),
            emit="post_refresh",
            alias_field=F(py_type=str),
            mask_last=None,
        ),
    )

    digest_of = staticmethod(credential_digest)
