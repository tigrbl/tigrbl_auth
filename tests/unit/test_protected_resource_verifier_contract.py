from __future__ import annotations

from types import SimpleNamespace
from uuid import uuid4

import pytest

from tigrbl_auth.config.deployment import resolve_deployment
from tigrbl_identity_storage.tables.token_record import _introspection as introspection_module
from tigrbl_auth.standards.oauth2.resource_verifier_contract import build_protected_resource_verifier_contract
from tigrbl_identity_storage_runtime.metadata.protected_resource_metadata import (
    build_protected_resource_metadata,
)


def _request_with_headers(headers: dict[str, str]) -> object:
    return SimpleNamespace(headers=headers, app=SimpleNamespace(state=SimpleNamespace()))


def test_verifier_contract_exposes_sender_constraint_and_introspection_policy() -> None:
    deployment = resolve_deployment(profile="fapi2-security")
    contract = build_protected_resource_verifier_contract(deployment)

    assert contract.sender_constraint_required is True
    assert "dpop" in contract.sender_constraint_modes
    assert "mtls" in contract.sender_constraint_modes
    assert "cnf" in contract.required_claims
    assert "private_key_jwt" in contract.introspection_auth_methods


def test_rfc9728_metadata_projection_matches_verifier_contract() -> None:
    deployment = resolve_deployment(profile="production")
    contract = build_protected_resource_verifier_contract(deployment)
    metadata = build_protected_resource_metadata(deployment)

    assert metadata["verifier_logic"] == contract.verifier_logic_id
    assert metadata["token_types_supported"] == list(contract.accepted_token_classes)
    assert metadata["required_claims"] == list(contract.required_claims)
    assert metadata["verification_freshness_expectation"] == contract.freshness_expectation


@pytest.mark.asyncio
async def test_introspection_rejects_basic_auth_when_verifier_contract_requires_private_key_jwt(monkeypatch: pytest.MonkeyPatch) -> None:
    contract = SimpleNamespace(introspection_auth_methods=("private_key_jwt",))
    client_id = str(uuid4())
    secret = "client-secret"
    basic = "Basic Y2xpZW50OmNsaWVudC1zZWNyZXQ="

    class _Client:
        id = client_id

        def verify_secret(self, provided: str) -> bool:
            return provided == secret

    monkeypatch.setattr(introspection_module, "_protected_resource_verifier_contract", lambda request: contract)
    async def _load_client(db, cid):
        return _Client(), SimpleNamespace(registration_metadata={})

    monkeypatch.setattr(introspection_module, "_load_client", _load_client)
    monkeypatch.setattr(introspection_module, "_registered_token_endpoint_auth_method", lambda registration: "client_secret_basic")

    request = _request_with_headers({"Authorization": basic})
    with pytest.raises(introspection_module.HTTPException) as exc_info:
        await introspection_module._authorize_introspection_caller(request, {"token": "tok"}, db=None)
    assert exc_info.value.status_code == 401


@pytest.mark.asyncio
async def test_introspection_accepts_basic_auth_when_verifier_contract_allows_it(monkeypatch: pytest.MonkeyPatch) -> None:
    contract = SimpleNamespace(introspection_auth_methods=("client_secret_basic", "client_secret_post"))
    client_id = str(uuid4())
    secret = "client-secret"
    basic = "Basic " + "Og=="

    class _Client:
        id = client_id

        def verify_secret(self, provided: str) -> bool:
            return provided == secret

    async def _load_client(db, cid):
        assert cid == client_id
        return _Client(), SimpleNamespace(registration_metadata={})

    monkeypatch.setattr(introspection_module, "_protected_resource_verifier_contract", lambda request: contract)
    monkeypatch.setattr(introspection_module, "_load_client", _load_client)
    monkeypatch.setattr(introspection_module, "_registered_token_endpoint_auth_method", lambda registration: "client_secret_basic")
    monkeypatch.setattr(introspection_module.base64, "b64decode", lambda value: f"{client_id}:{secret}".encode())

    request = _request_with_headers({"Authorization": basic})
    await introspection_module._authorize_introspection_caller(request, {"token": "tok"}, db=None)
