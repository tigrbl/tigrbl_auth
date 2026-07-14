from __future__ import annotations

from types import SimpleNamespace

import pytest

import tigrbl_identity_server.security.pushed_authorization as composition


@pytest.mark.asyncio
async def test_runtime_composes_durable_par_and_audit_operations(monkeypatch) -> None:
    persisted = []
    audited = []
    db = object()

    async def persist(ctx):
        persisted.append(ctx)
        return {
            "id": "par-1",
            "request_uri": "urn:ietf:params:oauth:request_uri:abc",
            "expires_in": 90,
        }

    async def audit(ctx):
        audited.append(ctx)

    monkeypatch.setattr(composition, "persist_pushed_authorization_request", persist)
    monkeypatch.setattr(composition, "append_audit_event_record", audit)

    service = composition.build_rfc9126_pushed_authorization_service(
        db,
        SimpleNamespace(enable_rfc9126=True),
    )
    result = await service.push(
        client_id="client-1",
        tenant_id="tenant-1",
        params={"scope": "openid", "audience": "api"},
    )

    assert result.record_id == "par-1"
    assert persisted == [
        {
            "payload": {
                "client_id": "client-1",
                "tenant_id": "tenant-1",
                "params": {"scope": "openid", "audience": "api"},
            },
            "db": db,
        }
    ]
    assert audited[0]["db"] is db
    assert audited[0]["payload"]["actor_client_id"] == "client-1"
    assert audited[0]["payload"]["details"]["audience"] == "api"


def test_runtime_composes_rfc9126_feature_state() -> None:
    service = composition.build_rfc9126_pushed_authorization_service(
        object(),
        SimpleNamespace(enable_rfc9126=False),
    )

    assert service.enabled is False
    assert service.capability.capability_report()["capability_id"] == (
        "oauth.pushed-authorization"
    )
