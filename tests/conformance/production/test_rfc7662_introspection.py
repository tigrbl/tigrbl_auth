from __future__ import annotations

from tigrbl_auth.config.deployment import resolve_deployment
from tigrbl_auth.standards.oauth2.introspection import _protected_resource_verifier_contract
from tigrbl_auth.standards.oauth2.resource_verifier_contract import build_protected_resource_verifier_contract


def test_rfc7662_introspection_uses_protected_resource_verifier_contract() -> None:
    deployment = resolve_deployment(profile="production")
    contract = build_protected_resource_verifier_contract(deployment)

    assert contract.accepted_token_classes == ("access_token",)
    assert "iss" in contract.required_claims
    assert "aud" in contract.required_claims
    assert contract.introspection_auth_methods


def test_rfc7662_introspection_contract_is_request_scoped() -> None:
    deployment = resolve_deployment(profile="fapi2-security")
    request = type(
        "_Request",
        (),
        {"app": type("_App", (), {"state": type("_State", (), {"tigrbl_auth_deployment": deployment})()})()},
    )()
    contract = _protected_resource_verifier_contract(request)

    assert contract.issuer == deployment.issuer
    assert contract.sender_constraint_required is True
    assert "private_key_jwt" in contract.introspection_auth_methods
