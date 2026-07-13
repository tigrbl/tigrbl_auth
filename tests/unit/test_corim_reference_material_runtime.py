from __future__ import annotations

import asyncio

from tigrbl_identity_storage.tables import (
    AttestationEndorsement,
    AttestationReferenceManifest,
    AttestationReferenceValue,
)
from tigrbl_identity_storage_runtime import publish_reference_material


def test_corim_reference_material_uses_one_table_transaction_context(monkeypatch) -> None:
    calls = []

    async def create(table, values, db):
        calls.append((table, dict(values), db))
        return dict(values)

    monkeypatch.setattr(AttestationReferenceManifest.handlers.create, "core", create)
    monkeypatch.setattr(AttestationReferenceValue.handlers.create, "core", create)
    monkeypatch.setattr(AttestationEndorsement.handlers.create, "core", create)

    db = object()
    result = asyncio.run(
        publish_reference_material(
            {
                "db": db,
                "payload": {
                    "manifest": {
                        "manifest_id": "corim-1",
                        "profile": "corim",
                        "format": "application/corim-unsigned+cbor",
                        "artifact_locator": "vault://corim/1",
                        "artifact_digest": "sha256:abc",
                    },
                    "reference_values": (
                        {
                            "environment": "device",
                            "measurement_id": "boot",
                            "algorithm": "sha-256",
                            "digest": "abc",
                        },
                    ),
                    "endorsements": (
                        {
                            "endorsement_id": "endorsement-1",
                            "profile": "corim",
                            "issuer": "manufacturer",
                            "artifact_locator": "vault://endorsement/1",
                            "artifact_digest": "sha256:def",
                        },
                    ),
                },
            }
        )
    )

    assert [call[0] for call in calls] == [
        AttestationReferenceManifest,
        AttestationReferenceValue,
        AttestationEndorsement,
    ]
    assert all(call[2] is db for call in calls)
    assert calls[1][1]["manifest_id"] == "corim-1"
    assert result["manifest"]["manifest_id"] == "corim-1"
