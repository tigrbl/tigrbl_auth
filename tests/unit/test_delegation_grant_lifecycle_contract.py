from __future__ import annotations

import asyncio
import importlib
from pathlib import Path
from types import SimpleNamespace
from uuid import uuid4

import pytest

from tigrbl_identity_contracts.delegation import (
    DelegationGrantLifecycleEntry,
    DelegationGrantSpec,
    normalize_delegation_scopes,
)


ROOT = Path(__file__).resolve().parents[2]


class _FakeTableHandlers:
    def __init__(self) -> None:
        self.rows: list[dict[str, object]] = []
        self.create = SimpleNamespace(core=self._create)
        self.list = SimpleNamespace(core=self._list)
        self.read = SimpleNamespace(core=self._read)
        self.update = SimpleNamespace(core=self._update)

    async def _create(self, ctx: dict[str, object]) -> dict[str, object]:
        payload = dict(ctx.get("payload") or {})
        payload.setdefault("id", uuid4())
        self.rows.append(payload)
        return payload

    async def _list(self, ctx: dict[str, object]) -> dict[str, object]:
        return {"items": list(self.rows)}

    async def _read(self, ctx: dict[str, object]) -> dict[str, object] | None:
        ident = (ctx.get("path_params") or {}).get("id")  # type: ignore[union-attr]
        return next((row for row in self.rows if str(row.get("id")) == str(ident)), None)

    async def _update(self, ctx: dict[str, object]) -> dict[str, object] | None:
        ident = (ctx.get("path_params") or {}).get("id")  # type: ignore[union-attr]
        payload = dict(ctx.get("payload") or {})
        for row in self.rows:
            if str(row.get("id")) == str(ident):
                row.update(payload)
                return row
        return None


async def _op(model, operation: str, db, **payload):
    return await getattr(model, operation)({"payload": payload, "db": db})


def test_delegation_lifecycle_dtos_are_contract_owned() -> None:
    authz_lifecycle = importlib.import_module("tigrbl_authz_policy.delegation")
    contracts = importlib.import_module("tigrbl_identity_contracts.delegation")

    assert authz_lifecycle.DelegationGrantLifecycleEntry is contracts.DelegationGrantLifecycleEntry
    assert authz_lifecycle.DelegationLifecycleAuditEvent is contracts.DelegationLifecycleAuditEvent
    assert authz_lifecycle.DelegationTokenLink is contracts.DelegationTokenLink
    assert authz_lifecycle.normalize_delegation_scopes is contracts.normalize_delegation_scopes
    assert not (
        ROOT
        / "pkgs"
        / "40-capabilities"
        / "tigrbl-authz-policy"
        / "src"
        / "tigrbl_authz_policy"
        / "_delegation_lifecycle_models.py"
    ).exists()
    assert not (
        ROOT
        / "pkgs"
        / "40-capabilities"
        / "tigrbl-authz-policy"
        / "src"
        / "tigrbl_authz_policy"
        / "_delegation_lifecycle_service.py"
    ).exists()


def test_delegation_grant_spec_contract_replaces_policy_grant_name() -> None:
    contracts = importlib.import_module("tigrbl_identity_contracts.delegation")
    authz_policy = importlib.import_module("tigrbl_authz_policy")
    facade = importlib.import_module("tigrbl_auth.services.formal_authorization")

    assert contracts.DelegationGrantSpec is DelegationGrantSpec
    assert authz_policy.DelegationGrantSpec is DelegationGrantSpec
    assert facade.DelegationGrantSpec is DelegationGrantSpec
    assert not hasattr(authz_policy, "DelegationGrant")
    assert not hasattr(authz_policy, "DelegationGrantLifecycleService")
    assert not hasattr(facade, "DelegationGrant")
    assert not hasattr(facade, "DelegationGrantLifecycleService")


def test_delegation_lifecycle_entry_converts_to_grant_spec() -> None:
    entry = DelegationGrantLifecycleEntry(
        grant_id="dgr:1",
        delegator="alice",
        delegate="bob",
        tenant_ids=("tenant-a",),
        actions=("client.read",),
        provenance_id="prov:1",
    )

    spec = entry.to_grant_spec()

    assert isinstance(spec, DelegationGrantSpec)
    assert spec.delegator == "alice"
    assert spec.delegate == "bob"
    assert spec.provenance_id == "prov:1"
    assert not hasattr(entry, "to_policy_grant")


def test_delegation_grant_storage_model_contract() -> None:
    storage_tables = importlib.import_module("tigrbl_identity_storage.tables")
    auth_tables = importlib.import_module("tigrbl_auth.tables")

    assert storage_tables.DelegationGrant.__tablename__ == "delegation_grants"
    assert storage_tables.DelegationGrantRecord is storage_tables.DelegationGrant
    assert auth_tables.DelegationGrant is storage_tables.DelegationGrant
    assert auth_tables.DelegationGrantRecord is storage_tables.DelegationGrant
    assert storage_tables.DelegationGrantScope.__tablename__ == "delegation_grant_scopes"
    assert storage_tables.DelegationGrantProof.__tablename__ == "delegation_grant_proofs"
    assert storage_tables.DelegationGrantEdge.__tablename__ == "delegation_grant_edges"
    assert storage_tables.DelegationGrantTokenLink.__tablename__ == "delegation_grant_token_links"

    metadata_tables = set(storage_tables.RestOltpTable.metadata.tables)
    assert {
        "authn.delegation_grants",
        "authn.delegation_grant_scopes",
        "authn.delegation_grant_proofs",
        "authn.delegation_grant_edges",
        "authn.delegation_grant_token_links",
    } <= metadata_tables


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


def test_delegation_grant_table_owns_lifecycle_and_association_ops(monkeypatch: pytest.MonkeyPatch) -> None:
    storage_tables = importlib.import_module("tigrbl_identity_storage.tables")
    grant_handlers = _FakeTableHandlers()
    edge_handlers = _FakeTableHandlers()
    proof_handlers = _FakeTableHandlers()
    token_link_handlers = _FakeTableHandlers()

    monkeypatch.setattr(storage_tables.DelegationGrant, "handlers", grant_handlers)
    monkeypatch.setattr(storage_tables.DelegationGrantEdge, "handlers", edge_handlers)
    monkeypatch.setattr(storage_tables.DelegationGrantProof, "handlers", proof_handlers)
    monkeypatch.setattr(storage_tables.DelegationGrantTokenLink, "handlers", token_link_handlers)

    async def scenario() -> None:
        state_grant = await _op(storage_tables.DelegationGrant, "create_grant",
            object(),
            delegator_subject="alice",
            delegate_subject="erin",
        )
        parent = await _op(storage_tables.DelegationGrant, "create_grant",
            object(),
            delegator_subject="alice",
            delegate_subject="bob",
            tenant_id=uuid4(),
        )
        child = await _op(storage_tables.DelegationGrant, "create_grant",
            object(),
            delegator_subject="bob",
            delegate_subject="carol",
            parent_grant_id=parent["id"],
        )
        await _op(storage_tables.DelegationGrantEdge, "link_edge",
            object(),
            parent_grant_id=parent["id"],
            child_grant_id=child["id"],
            delegator_subject="bob",
            delegate_subject="carol",
        )

        inspected = await _op(storage_tables.DelegationGrant, "inspect_grant", object(), grant_id=parent["id"])
        active = await _op(storage_tables.DelegationGrant, "activate_grant", object(), grant_id=state_grant["id"])
        active_status = active["status"]
        expired = await _op(storage_tables.DelegationGrant, "expire_grant", object(), grant_id=state_grant["id"])
        replacement = await _op(storage_tables.DelegationGrant, "replace_grant",
            object(),
            grant_id=child["id"],
            delegate_subject="dave",
        )
        revoked = await _op(storage_tables.DelegationGrant, "revoke_grant",
            object(),
            grant_id=parent["id"],
            revoked_by="admin",
            reason="cleanup",
            collapse_descendants=True,
        )
        grants = await _op(storage_tables.DelegationGrant, "list_grants",
            object(),
            delegator_subject="alice",
            delegate_subject="bob",
        )
        proof = await _op(storage_tables.DelegationGrantProof, "persist_provenance",
            object(),
            grant_id=parent["id"],
            source_scope_hash="source",
            delegated_scope_hash="delegated",
            attenuation_result=True,
            proof_hash="proof:1",
        )
        token_link = await _op(storage_tables.DelegationGrantTokenLink, "link_token",
            object(),
            grant_id=parent["id"],
            token_hash="token:hash",
            subject="bob",
        )
        token_links = await _op(storage_tables.DelegationGrantTokenLink, "list_for_grant", object(), grant_id=parent["id"])

        assert inspected is parent
        assert active_status == "active"
        assert expired["status"] == "expired"
        assert replacement["parent_grant_id"] == child["id"]
        assert revoked["status"] == "revoked"
        assert child["status"] in {"replaced", "revoked"}
        assert grants == [parent]
        assert proof["proof_hash"] == "proof:1"
        assert token_link in token_links
        assert edge_handlers.rows[0]["active"] is False

    asyncio.run(scenario())


def test_delegation_grant_oauth_boundary_no_policy_ownership_contract(monkeypatch: pytest.MonkeyPatch) -> None:
    oauth_exchange = importlib.import_module("tigrbl_identity_storage_runtime.token_exchange")

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
        lambda *args, **kwargs: SimpleNamespace(
            issuer="https://issuer.example",
            protected_resource_identifier="https://issuer.example/resource",
            flag_enabled=lambda flag: flag == "enable_rfc8693",
        ),
    )
    monkeypatch.setattr(
        oauth_exchange,
        "build_protected_resource_verifier_contract",
        lambda deployment: SimpleNamespace(
            verifier_logic_id="resource-verifier:test",
            required_claims=("iss", "sub", "aud", "exp", "iat"),
        ),
    )
    monkeypatch.setattr(oauth_exchange, "upsert_token_record_async", capture_token_record)
    monkeypatch.setattr(oauth_exchange, "append_audit_event_async", capture_audit_event)
    monkeypatch.setattr(
        oauth_exchange,
        "validate_sender_constraint",
        lambda *args, **kwargs: SimpleNamespace(
            mechanism="bearer",
            cert_thumbprint=None,
            confirmation_claim=None,
            token_type="Bearer",
        ),
    )

    request = SimpleNamespace(
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
