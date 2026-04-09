"""Dependency-light tests for RFC 7523 client assertion processing."""

from __future__ import annotations

import time
from unittest.mock import patch

import pytest

from tigrbl_auth import encode_jwt
from tigrbl_auth.errors import InvalidTokenError
from tigrbl_auth.rfc.rfc7523 import (
    JWT_BEARER_ASSERTION_TYPE,
    PRIVATE_KEY_JWT_AUTH_METHOD,
    RFC7523_SPEC_URL,
    authenticate_client_assertion,
    build_client_assertion_contract_examples,
    token_endpoint_auth_methods_supported,
    token_endpoint_auth_signing_alg_values_supported,
    validate_client_jwt_bearer,
)
from tigrbl_auth.runtime_cfg import settings


@pytest.mark.unit
def test_validate_client_jwt_bearer_success_with_strict_claims() -> None:
    token = encode_jwt(
        iss="client",
        sub="client",
        aud="https://issuer.example/token",
        exp=int(time.time()) + 60,
        iat=int(time.time()),
        jti="assertion-1",
    )
    claims = validate_client_jwt_bearer(
        token,
        audience="https://issuer.example/token",
        client_id="client",
        require_strict_claims=True,
    )
    assert claims["iss"] == "client"
    assert RFC7523_SPEC_URL.startswith("https://")


@pytest.mark.unit
def test_validate_client_jwt_bearer_missing_required_claim() -> None:
    token = encode_jwt(iss="client", sub="client", exp=int(time.time()) + 60)
    with pytest.raises(ValueError):
        validate_client_jwt_bearer(token, audience="https://issuer.example/token")


@pytest.mark.unit
def test_validate_client_jwt_bearer_missing_strict_jti() -> None:
    with pytest.raises(ValueError):
        validate_client_jwt_bearer(
            "unused-token",
            audience="https://issuer.example/token",
            client_id="client",
            require_strict_claims=True,
            decoder=lambda _: {
                "iss": "client",
                "sub": "client",
                "aud": "https://issuer.example/token",
                "exp": int(time.time()) + 60,
                "iat": int(time.time()),
            },
        )


@pytest.mark.unit
def test_validate_client_jwt_bearer_mismatched_subject() -> None:
    token = encode_jwt(
        iss="client-a",
        sub="client-b",
        aud="https://issuer.example/token",
        exp=int(time.time()) + 60,
    )
    with pytest.raises(ValueError):
        validate_client_jwt_bearer(token, audience="https://issuer.example/token")


@pytest.mark.unit
def test_validate_client_jwt_bearer_invalid_audience() -> None:
    token = encode_jwt(
        iss="client",
        sub="client",
        aud="https://issuer.example/token",
        exp=int(time.time()) + 60,
    )
    with pytest.raises(ValueError):
        validate_client_jwt_bearer(token, audience="https://other.example/token")


@pytest.mark.unit
def test_validate_client_jwt_bearer_client_id_mismatch() -> None:
    token = encode_jwt(
        iss="client",
        sub="client",
        aud="https://issuer.example/token",
        exp=int(time.time()) + 60,
    )
    with pytest.raises(ValueError):
        validate_client_jwt_bearer(token, audience="https://issuer.example/token", client_id="other-client")


@pytest.mark.unit
def test_validate_client_jwt_bearer_expired_assertion() -> None:
    token = encode_jwt(
        iss="client",
        sub="client",
        aud="https://issuer.example/token",
        exp=int(time.time()) - 1,
        iat=int(time.time()) - 5,
        jti="assertion-2",
    )
    with pytest.raises(InvalidTokenError):
        validate_client_jwt_bearer(
            token,
            audience="https://issuer.example/token",
            client_id="client",
            require_strict_claims=True,
        )


@pytest.mark.unit
def test_authenticate_client_assertion_rejects_wrong_type() -> None:
    token = encode_jwt(
        iss="client",
        sub="client",
        aud="https://issuer.example/token",
        exp=int(time.time()) + 60,
        iat=int(time.time()),
        jti="assertion-3",
    )
    with pytest.raises(ValueError):
        authenticate_client_assertion(
            client_assertion_type="unsupported",
            client_assertion=token,
            audience="https://issuer.example/token",
            client_id="client",
            token_endpoint_auth_method=PRIVATE_KEY_JWT_AUTH_METHOD,
        )


@pytest.mark.unit
def test_supported_metadata_surfaces_reflect_runtime_support() -> None:
    assert PRIVATE_KEY_JWT_AUTH_METHOD in token_endpoint_auth_methods_supported()
    assert token_endpoint_auth_signing_alg_values_supported() == ["EdDSA"]
    example = build_client_assertion_contract_examples("https://issuer.example/token")[0]
    assert example["client_assertion_type"] == JWT_BEARER_ASSERTION_TYPE


@pytest.mark.unit
def test_validate_client_jwt_bearer_disabled() -> None:
    token = encode_jwt(
        iss="client",
        sub="client",
        aud="https://issuer.example/token",
        exp=int(time.time()) + 60,
    )
    with patch.object(settings, "enable_rfc7523", False):
        with pytest.raises(RuntimeError):
            validate_client_jwt_bearer(token, audience="https://issuer.example/token")
