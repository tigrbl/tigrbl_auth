from __future__ import annotations

from contextlib import asynccontextmanager

import pytest

from tigrbl_identity_contracts.attestation import ReferenceIntegrityManifest
from tigrbl_identity_storage_runtime import CorimReferenceMaterialRepository


class _Store:
    def __init__(self) -> None:
        self.rows: dict[type, list[dict[str, object]]] = {}

    async def insert(self, table, values):
        row = dict(values)
        self.rows.setdefault(table, []).append(row)
        return row

    async def get(self, table, identifier):
        return None

    async def update(self, table, identifier, values):
        raise NotImplementedError

    async def list(self, table, filters):
        return [
            row for row in self.rows.get(table, ())
            if all(row.get(key) == value for key, value in filters.items())
        ]


class _Transactions:
    def __init__(self) -> None:
        self.commits = 0

    @asynccontextmanager
    async def transaction(self):
        yield
        self.commits += 1


@pytest.mark.asyncio
async def test_corim_publication_is_atomic_durable_and_immutable() -> None:
    store, transactions = _Store(), _Transactions()
    repository = CorimReferenceMaterialRepository(store, transactions)
    manifest = ReferenceIntegrityManifest("corim-1", ({"tag-type": "comid"},), "issuer")

    row = await repository.publish(
        manifest,
        artifact_locator="immutable://corim/1",
        artifact_digest="sha256:abc",
        profile="draft-ietf-rats-corim-11",
        reference_values=(
            {
                "environment": "device-class-a",
                "measurement_id": "boot",
                "algorithm": "sha-256",
                "digest": "abc",
            },
        ),
        endorsements=(
            {
                "endorsement_id": "endorsement-1",
                "issuer": "manufacturer",
                "artifact_locator": "immutable://endorsement/1",
                "artifact_digest": "sha256:def",
            },
        ),
    )

    assert row["manifest_id"] == "corim-1"
    assert repository.persistence == "durable"
    assert transactions.commits == 1

    with pytest.raises(ValueError, match="immutable once published"):
        await repository.publish(
            manifest,
            artifact_locator="immutable://corim/replacement",
            artifact_digest="sha256:replacement",
            profile="draft-ietf-rats-corim-11",
        )
