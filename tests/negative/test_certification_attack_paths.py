from __future__ import annotations

from types import SimpleNamespace

import pytest
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ed25519

from tigrbl_auth.config.deployment import resolve_deployment
from tigrbl_auth.errors import InvalidTokenError
from tigrbl_auth.standards.oauth2.dpop import clear_runtime_state, jwk_from_public_key, jwk_thumbprint, make_proof
from tigrbl_auth.standards.oauth2.issuer_identification import IssuerIdentificationError, extract_issuer_from_redirect_uri
from tigrbl_auth.standards.oauth2.jwt_access_tokens import validate_jwt_access_token_claims
from tigrbl_auth.standards.oauth2.rfc9700 import (
    OAuthPolicyViolation,
    assert_authorization_request_allowed,
    assert_token_request_allowed,
    verify_access_token_sender_constraint,
)


def _ed25519_keyref() -> SimpleNamespace:
    private_key = ed25519.Ed25519PrivateKey.generate()
    private_pem = private_key.private_bytes(
        serialization.Encoding.PEM,
        serialization.PrivateFormat.PKCS8,
        serialization.NoEncryption(),
    )
    public_pem = private_key.public_key().public_bytes(
        serialization.Encoding.PEM,
        serialization.PublicFormat.SubjectPublicKeyInfo,
    )
    return SimpleNamespace(material=private_pem, public=public_pem)


def test_fapi_profile_rejects_par_bypass_attempts() -> None:
    deployment = resolve_deployment(None, profile="fapi2-security")
    with pytest.raises(OAuthPolicyViolation) as excinfo:
        assert_authorization_request_allowed(
            {
                "_frontchannel_request": True,
                "response_type": "code",
                "client_id": "client-a",
                "request_uri": "urn:ietf:params:oauth:request_uri:test",
                "redirect_uri": "https://client.example/cb",
                "scope": "openid",
                "code_challenge": "challenge",
                "code_challenge_method": "S256",
            },
            deployment,
        )
    assert excinfo.value.error == "invalid_request"


def test_fapi_profile_rejects_implicit_hybrid_and_password_grants() -> None:
    deployment = resolve_deployment(None, profile="fapi2-security")
    with pytest.raises(OAuthPolicyViolation) as implicit_exc:
        assert_authorization_request_allowed(
            {
                "response_type": "code token",
                "client_id": "client-a",
                "request_uri": "urn:ietf:params:oauth:request_uri:test",
                "code_challenge": "challenge",
                "code_challenge_method": "S256",
            },
            deployment,
        )
    assert implicit_exc.value.error == "unsupported_response_type"

    with pytest.raises(OAuthPolicyViolation) as password_exc:
        assert_token_request_allowed({"grant_type": "password"}, deployment)
    assert password_exc.value.error == "unsupported_grant_type"


def test_wrong_audience_access_tokens_fail_closed() -> None:
    payload = {
        "iss": "https://issuer.example",
        "aud": "https://other-resource.example",
        "sub": "user-1",
        "exp": 1,
    }
    with pytest.raises(InvalidTokenError):
        validate_jwt_access_token_claims(
            payload,
            issuer="https://issuer.example",
            audience="https://resource.example",
        )


def test_wrong_issuer_mix_up_redirect_is_rejected() -> None:
    with pytest.raises(IssuerIdentificationError):
        extract_issuer_from_redirect_uri(
            "https://client.example/cb?code=abc&iss=https%3A%2F%2Fevil.example",
            "https://issuer.example",
        )


def test_sender_constrained_bearer_replay_and_wrong_key_fail_closed() -> None:
    clear_runtime_state()
    deployment = resolve_deployment(None, profile="fapi2-security")
    request = SimpleNamespace(method="GET", url="https://rs.example.com/resource", headers={})

    key_a = _ed25519_keyref()
    key_b = _ed25519_keyref()
    jkt_a = jwk_thumbprint(jwk_from_public_key(key_a.public))
    access_token = "capability-access-token"
    proof_a = make_proof(key_a, "GET", "https://rs.example.com/resource", access_token=access_token)
    proof_b = make_proof(key_b, "GET", "https://rs.example.com/resource", access_token=access_token)
    token_payload = {"cnf": {"jkt": jkt_a}}

    assert verify_access_token_sender_constraint(
        request,
        token_payload,
        deployment,
        access_token=access_token,
        dpop_proof=proof_a,
    ).jkt == jkt_a

    with pytest.raises(OAuthPolicyViolation):
        verify_access_token_sender_constraint(
            request,
            token_payload,
            deployment,
            access_token=access_token,
            dpop_proof=proof_a,
        )

    with pytest.raises(OAuthPolicyViolation):
        verify_access_token_sender_constraint(
            request,
            token_payload,
            deployment,
            access_token=access_token,
            dpop_proof=proof_b,
        )
