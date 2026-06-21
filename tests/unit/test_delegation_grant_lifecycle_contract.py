from __future__ import annotations

import asyncio
import importlib
import types

import pytest

from tigrbl_authz_policy import AuthorityScope
from tigrbl_authz_policy.delegation_lifecycle import (
    DelegationGrantLifecycleService,
    assert_delegation_management_surface,
    delegation_grant_uix_workflows,
    normalize_delegation_scopes,
)


def _grant_service() -> DelegationGrantLifecycleService:
    return DelegationGrantLifecycleService()


def test_delegation_grant_storage_model_contract() -> None:
    storage_tables = importlib.import_module("tigrbl_identity_storage.tables")
    auth_tables = importlib.import_module("tigrbl_auth.tables")

    assert storage_tables.DelegationGrantRecord.__tablename__ == "delegation_grants"
    assert storage_tables.DelegationGrantScope.__tablename__ == "delegation_grant_scopes"
    assert storage_tables.DelegationGrantProof.__tablename__ == "delegation_grant_proofs"
    assert storage_tables.DelegationGrantEdge.__tablename__ == "delegation_grant_edges"
    assert storage_tables.DelegationGrantTokenLink.__tablename__ == "delegation_grant_token_links"
    assert auth_tables.DelegationGrantRecord is storage_tables.DelegationGrantRecord

    metadata_tables = set(storage_tables.RestOltpTable.metadata.tables)
    assert {
        "authn.delegation_grants",
        "authn.delegation_grant_scopes",
        "authn.delegation_grant_proofs",
        "authn.delegation_grant_edges",
        "authn.delegation_grant_token_links",
    } <= metadata_tables


def test_delegation_grant_lifecycle_service_contract() -> None:
    service = _grant_service()
    grant = service.create(
        delegator="alice",
        delegate="bob",
        tenant_ids=["tenant-a"],
        actions=["client.read"],
        resources=["client:123"],
        policy_version="v1",
        provenance_id="prov:known",
        actor="admin",
    )

    evaluation = service.evaluate(
        grant.grant_id,
        source_scopes=[AuthorityScope("tenant-a", "client.*", "client:123", "")],
        known_provenance_ids=["prov:known"],
        allowed_policy_versions=["v1"],
    )

    assert service.inspect(grant.grant_id).active is True
    assert evaluation.allowed is True
    assert evaluation.proof_hash
    assert "delegation.grant.created" in {event.event_type for event in service.audit_events(grant.grant_id)}
    assert "delegation.grant.evaluation.allowed" in {
        event.event_type for event in service.audit_events(grant.grant_id)
    }


def test_delegation_grant_scope_normalization_contract() -> None:
    scopes = normalize_delegation_scopes(
        tenant_ids=["tenant-b", "tenant-a", "tenant-a"],
        actions=["client.write", "client.read", "client.read"],
        resources=["client:2", "client:1"],
        realm="primary",
    )

    assert [scope.key for scope in scopes] == [
        ("tenant-a", "primary", "client.read", "client:1"),
        ("tenant-a", "primary", "client.read", "client:2"),
        ("tenant-a", "primary", "client.write", "client:1"),
        ("tenant-a", "primary", "client.write", "client:2"),
        ("tenant-b", "primary", "client.read", "client:1"),
        ("tenant-b", "primary", "client.read", "client:2"),
        ("tenant-b", "primary", "client.write", "client:1"),
        ("tenant-b", "primary", "client.write", "client:2"),
    ]

    with pytest.raises(ValueError):
        normalize_delegation_scopes(tenant_ids=[], actions=["client.read"])


def test_delegation_grant_revocation_collapse_contract() -> None:
    service = _grant_service()
    parent = service.create(
        delegator="alice",
        delegate="bob",
        tenant_ids=["tenant-a"],
        actions=["client.read"],
    )
    child = service.create(
        delegator="bob",
        delegate="carol",
        tenant_ids=["tenant-a"],
        actions=["client.read"],
        parent_grant_id=parent.grant_id,
    )

    revoked_ids = service.revoke(parent.grant_id, actor="admin", reason="security")

    assert revoked_ids == (parent.grant_id, child.grant_id)
    assert service.inspect(parent.grant_id).active is False
    assert service.inspect(child.grant_id).active is False
    with pytest.raises(ValueError):
        service.link_token(child.grant_id, token="issued-token", subject="carol")


def test_delegation_grant_token_linkage_contract() -> None:
    service = _grant_service()
    grant = service.create(
        delegator="alice",
        delegate="bob",
        tenant_ids=["tenant-a"],
        actions=["client.read"],
    )

    link = service.link_token(
        grant.grant_id,
        token="issued-token",
        subject="bob",
        actor_subject="alice",
        authorization_trace_id="trace:1",
        delegation_provenance_id="lineage:1",
        source_token="subject-token",
        actor_token="actor-token",
    )

    claims = link.as_claims()
    assert claims["delegation_grant_id"] == grant.grant_id
    assert claims["authorization_trace_id"] == "trace:1"
    assert claims["delegation_provenance_id"] == "lineage:1"
    assert claims["actor_subject"] == "alice"
    assert claims["source_token_hash"] != "subject-token"
    assert claims["actor_token_hash"] != "actor-token"


def test_delegation_grant_management_api_boundary_contract() -> None:
    service = _grant_service()
    grant = service.create(
        delegator="alice",
        delegate="bob",
        tenant_ids=["tenant-a"],
        actions=["client.read"],
    )

    projection = service.management_projection(grant.grant_id, surface="tenant-admin-api")

    assert projection["id"] == grant.grant_id
    assert projection["status"] == "active"
    assert projection["active"] is True
    with pytest.raises(PermissionError):
        assert_delegation_management_surface("oauth-token-endpoint")


def test_delegation_grant_audit_events_contract() -> None:
    service = _grant_service()
    grant = service.create(
        delegator="alice",
        delegate="bob",
        tenant_ids=["tenant-a"],
        actions=["client.read"],
        actor="admin",
    )
    service.evaluate(
        grant.grant_id,
        source_scopes=[AuthorityScope("tenant-a", "client.read", "*", "")],
    )
    service.revoke(grant.grant_id, actor="admin", reason="cleanup")

    events = service.audit_events(grant.grant_id)
    assert [event.event_type for event in events] == [
        "delegation.grant.created",
        "delegation.grant.activated",
        "delegation.grant.evaluation.allowed",
        "delegation.grant.revoked",
    ]
    assert events[-1].reason == "cleanup"


def test_delegation_grant_uix_workflows_contract() -> None:
    workflows = delegation_grant_uix_workflows(surface="platform-admin-api")

    assert {workflow["workflow"] for workflow in workflows} == {
        "list",
        "inspect",
        "create",
        "replace",
        "revoke",
    }
    assert all(workflow["api_owned"] is True for workflow in workflows)


def test_delegation_grant_cross_tenant_denial_contract() -> None:
    service = _grant_service()
    grant = service.create(
        delegator="alice",
        delegate="bob",
        tenant_ids=["tenant-b"],
        actions=["client.read"],
    )

    evaluation = service.evaluate(
        grant.grant_id,
        source_scopes=[AuthorityScope("tenant-a", "client.*", "*", "")],
    )

    assert evaluation.allowed is False
    assert evaluation.proof.uncovered_scopes
    assert "not covered in tenant 'tenant-b'" in " ".join(evaluation.failures)


def test_delegation_grant_oauth_boundary_no_policy_ownership_contract(monkeypatch: pytest.MonkeyPatch) -> None:
    oauth_exchange = importlib.import_module("tigrbl_identity_storage.tables.token_record._token_exchange")

    class FakeJwt:
        async def async_decode(self, token: str, verify_exp: bool = True) -> dict[str, object]:
            if token == "subject-token":
                return {
                    "sub": "bob",
                    "tid": "tenant-a",
                    "scope": "client.read",
                    "iss": "issuer-a",
                    "delegation_grant_id": "dgr:stored",
                }
            return {"sub": "alice", "tid": "tenant-a", "iss": "issuer-a"}

        async def async_sign(self, **kwargs: object) -> str:
            return "issued-token"

    captured: dict[str, object] = {}

    async def capture_token_record(token: str, claims: dict[str, object], **kwargs: object) -> None:
        captured["token"] = token
        captured["claims"] = claims

    async def capture_audit_event(**kwargs: object) -> None:
        captured["audit"] = kwargs

    monkeypatch.setattr(oauth_exchange, "_jwt_coder", FakeJwt())
    monkeypatch.setattr(
        oauth_exchange,
        "deployment_from_request",
        lambda *args, **kwargs: types.SimpleNamespace(
            issuer="https://issuer.example",
            protected_resource_identifier="https://issuer.example/resource",
            flag_enabled=lambda flag: flag == "enable_rfc8693",
        ),
    )
    monkeypatch.setattr(
        oauth_exchange,
        "build_protected_resource_verifier_contract",
        lambda deployment: types.SimpleNamespace(
            verifier_logic_id="resource-verifier:test",
            required_claims=("iss", "sub", "aud", "exp", "iat"),
        ),
    )
    monkeypatch.setattr(oauth_exchange, "upsert_token_record_async", capture_token_record)
    monkeypatch.setattr(oauth_exchange, "append_audit_event_async", capture_audit_event)
    monkeypatch.setattr(
        oauth_exchange,
        "validate_sender_constraint",
        lambda *args, **kwargs: types.SimpleNamespace(
            mechanism="bearer",
            cert_thumbprint=None,
            confirmation_claim=None,
            token_type="Bearer",
        ),
    )

    request = types.SimpleNamespace(
        body=(
            b"grant_type=urn:ietf:params:oauth:grant-type:token-exchange"
            b"&subject_token=subject-token"
            b"&subject_token_type=urn:ietf:params:oauth:token-type:access_token"
            b"&actor_token=actor-token"
            b"&requested_token_type=access_token"
            b"&delegation_grant_id=dgr:stored"
        ),
        method="POST",
        url="https://issuer.example/token/exchange",
        headers={},
    )

    response = asyncio.run(oauth_exchange.token_exchange(request))

    claims = captured["claims"]
    linkage = claims["delegation_token_linkage"]
    assert response["access_token"] == "issued-token"
    assert claims["delegation_grant_id"] == "dgr:stored"
    assert linkage["delegation_grant_id"] == "dgr:stored"
    assert linkage["source_token_hash"] != "subject-token"
    assert linkage["actor_token_hash"] != "actor-token"
    assert "DelegationGrantLifecycleService" not in oauth_exchange.__dict__
