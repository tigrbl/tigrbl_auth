from __future__ import annotations

from types import SimpleNamespace
from urllib.parse import urlencode

import pytest

from tigrbl_auth.services.authorization_provenance import (
    build_authorization_decision_trace,
    build_delegation_provenance,
)
import tigrbl_identity_server.token_exchange_runtime as token_exchange_mod


class _FakeRequest:
    def __init__(self, *, body: bytes):
        self.body = body
        self.headers: dict[str, str] = {}
        self.method = "POST"
        self.url = "https://issuer.example/token/exchange"


class _FakeDeployment:
    issuer = "https://issuer.example/tenants/acme"

    def flag_enabled(self, flag: str) -> bool:
        return flag == "enable_rfc8693"


class _FakeSenderConstraint:
    confirmation_claim = None
    cert_thumbprint = None
    token_type = "bearer"
    mechanism = "dpop"


@pytest.mark.unit
def test_authorization_decision_trace_is_deterministic() -> None:
    first = build_authorization_decision_trace(
        tenant_id="tenant-a",
        subject="user-1",
        issuer="https://issuer.example/tenants/acme",
        audience="https://rs.example",
        resource="https://rs.example",
        scope="read write",
        subject_token_type="urn:ietf:params:oauth:token-type:access_token",
        requested_token_type="access_token",
        exchange_mode="delegation",
        actor_subject="actor-1",
        source_issuer="https://issuer.example/root",
        sender_constraint="dpop",
        verifier_logic_id="protected-resource-verifier",
        required_claims=("sub", "iss", "aud"),
    )
    second = build_authorization_decision_trace(
        tenant_id="tenant-a",
        subject="user-1",
        issuer="https://issuer.example/tenants/acme",
        audience="https://rs.example",
        resource="https://rs.example",
        scope="read write",
        subject_token_type="urn:ietf:params:oauth:token-type:access_token",
        requested_token_type="access_token",
        exchange_mode="delegation",
        actor_subject="actor-1",
        source_issuer="https://issuer.example/root",
        sender_constraint="dpop",
        verifier_logic_id="protected-resource-verifier",
        required_claims=("sub", "iss", "aud"),
    )
    assert first["decision_key"] == second["decision_key"]
    assert first["request_hash"] == second["request_hash"]
    assert first["policy_hash"] == second["policy_hash"]


@pytest.mark.unit
def test_delegation_provenance_changes_when_actor_changes() -> None:
    trace = build_authorization_decision_trace(
        tenant_id="tenant-a",
        subject="user-1",
        issuer="https://issuer.example/tenants/acme",
        audience="https://rs.example",
        resource="https://rs.example",
        scope="read",
        subject_token_type="urn:ietf:params:oauth:token-type:access_token",
        requested_token_type="access_token",
        exchange_mode="delegation",
        actor_subject="actor-1",
        source_issuer="https://issuer.example/root",
        sender_constraint="none",
    )
    first = build_delegation_provenance(
        subject_token="subject-token",
        actor_token="actor-token-a",
        subject_claims={"sub": "user-1", "iss": "https://issuer.example/root", "aud": "https://rs.example"},
        actor_claims={"sub": "actor-1", "iss": "https://issuer.example/root"},
        authorization_trace=trace,
        audience="https://rs.example",
        resource="https://rs.example",
        exchange_mode="delegation",
        sender_constraint="none",
    )
    second = build_delegation_provenance(
        subject_token="subject-token",
        actor_token="actor-token-b",
        subject_claims={"sub": "user-1", "iss": "https://issuer.example/root", "aud": "https://rs.example"},
        actor_claims={"sub": "actor-2", "iss": "https://issuer.example/root"},
        authorization_trace=trace,
        audience="https://rs.example",
        resource="https://rs.example",
        exchange_mode="delegation",
        sender_constraint="none",
    )
    assert first["lineage_id"] != second["lineage_id"]


@pytest.mark.asyncio
@pytest.mark.unit
async def test_token_exchange_runtime_persists_authorization_trace_and_delegation_provenance(monkeypatch) -> None:
    persisted: dict[str, object] = {}
    audited: dict[str, object] = {}

    class _JWT:
        async def async_decode(self, token, verify_exp=True):
            if token == "actor-token":
                return {"sub": "actor-1", "iss": "https://issuer.example/root"}
            return {
                "sub": "user-1",
                "tid": "tenant-a",
                "iss": "https://issuer.example/root",
                "aud": "https://rs.example",
                "scope": "read",
            }

        async def async_sign(self, **kwargs):
            return "access-token"

    async def _upsert(token, claims, **kwargs):
        persisted["token"] = token
        persisted["claims"] = claims
        persisted["kwargs"] = kwargs
        return "digest"

    async def _audit(**kwargs):
        audited.update(kwargs)

    monkeypatch.setattr(token_exchange_mod, "_jwt_coder", lambda: _JWT())
    monkeypatch.setattr(token_exchange_mod, "deployment_from_request", lambda request, settings: _FakeDeployment())
    monkeypatch.setattr(token_exchange_mod, "validate_sender_constraint", lambda *args, **kwargs: _FakeSenderConstraint())
    monkeypatch.setattr(
        token_exchange_mod,
        "build_protected_resource_verifier_contract",
        lambda deployment: SimpleNamespace(verifier_logic_id="protected-resource-verifier", required_claims=("sub", "iss", "aud")),
    )
    monkeypatch.setattr(token_exchange_mod, "upsert_token_record_async", _upsert)
    monkeypatch.setattr(token_exchange_mod, "append_audit_event_async", _audit)

    request = _FakeRequest(
        body=urlencode(
            {
                "grant_type": token_exchange_mod.TOKEN_EXCHANGE_GRANT_TYPE,
                "subject_token": "subject-token",
                "subject_token_type": "urn:ietf:params:oauth:token-type:access_token",
                "actor_token": "actor-token",
                "actor_token_type": "urn:ietf:params:oauth:token-type:access_token",
                "requested_token_type": "access_token",
                "audience": "https://rs.example",
                "resource": "https://rs.example",
            }
        ).encode("utf-8")
    )

    response = await token_exchange_mod.token_exchange(request)

    assert response["access_token"] == "access-token"
    claims = persisted["claims"]
    assert isinstance(claims, dict)
    assert claims["authorization_trace"]["decision_key"]
    assert claims["authorization_trace"]["request"]["issuer"] == "https://issuer.example/tenants/acme"
    assert claims["delegation_provenance"]["lineage_id"]
    assert claims["delegation_provenance"]["nodes"]["actor"]["sub"] == "actor-1"
    assert audited["request_id"] == claims["authorization_trace"]["request_hash"]
    assert audited["details"]["delegation_lineage_id"] == claims["delegation_provenance"]["lineage_id"]
