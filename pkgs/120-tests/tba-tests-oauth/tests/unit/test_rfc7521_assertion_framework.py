"""Dependency-light tests for RFC 7521 assertion processing."""

from __future__ import annotations

import time
from unittest.mock import patch

import pytest

from tba_auth import encode_jwt
from tba_auth.errors import InvalidTokenError
from tba_auth.rfc.rfc7521 import (
    JWT_BEARER_GRANT_TYPE,
    RFC7521_SPEC_URL,
    build_assertion_contract_examples,
    validate_assertion_grant_request,
    validate_jwt_assertion,
)
from tba_auth.runtime_cfg import settings


@pytest.mark.unit
def test_validate_jwt_assertion_success() -> None:
    token = encode_jwt(
        iss="issuer",
        sub="subject",
        tid="tenant",
        aud="https://issuer.example/token",
        exp=int(time.time()) + 60,
        iat=int(time.time()),
    )
    claims = validate_jwt_assertion(token, audience="https://issuer.example/token")
    assert claims["iss"] == "issuer"
    assert claims["sub"] == "subject"
    assert claims["aud"] == "https://issuer.example/token"
    assert RFC7521_SPEC_URL.startswith("https://")


@pytest.mark.unit
def test_validate_jwt_assertion_missing_claim() -> None:
    token = encode_jwt(iss="issuer", sub="subject", exp=int(time.time()) + 60)
    with pytest.raises(ValueError):
        validate_jwt_assertion(token)


@pytest.mark.unit
def test_validate_jwt_assertion_invalid_audience() -> None:
    token = encode_jwt(
        iss="issuer",
        sub="subject",
        aud="https://issuer.example/token",
        exp=int(time.time()) + 60,
    )
    with pytest.raises(ValueError):
        validate_jwt_assertion(token, audience="https://other.example/token")


@pytest.mark.unit
def test_validate_jwt_assertion_expired() -> None:
    token = encode_jwt(
        iss="issuer",
        sub="subject",
        aud="https://issuer.example/token",
        exp=int(time.time()) - 10,
    )
    with pytest.raises(InvalidTokenError):
        validate_jwt_assertion(token, audience="https://issuer.example/token")


@pytest.mark.unit
def test_validate_jwt_assertion_future_nbf_rejected() -> None:
    token = encode_jwt(
        iss="issuer",
        sub="subject",
        aud="https://issuer.example/token",
        exp=int(time.time()) + 60,
        nbf=int(time.time()) + 120,
    )
    with pytest.raises(InvalidTokenError):
        validate_jwt_assertion(token, audience="https://issuer.example/token")


@pytest.mark.unit
def test_validate_assertion_grant_request_requires_assertion_and_grant_type() -> None:
    with pytest.raises(ValueError):
        validate_assertion_grant_request({"grant_type": "authorization_code"}, audience="https://issuer.example/token")
    with pytest.raises(ValueError):
        validate_assertion_grant_request({"grant_type": JWT_BEARER_GRANT_TYPE}, audience="https://issuer.example/token")


@pytest.mark.unit
def test_validate_assertion_grant_request_success() -> None:
    token = encode_jwt(
        iss="issuer",
        sub="subject",
        aud="https://issuer.example/token",
        exp=int(time.time()) + 60,
    )
    claims = validate_assertion_grant_request(
        {"grant_type": JWT_BEARER_GRANT_TYPE, "assertion": token},
        audience="https://issuer.example/token",
    )
    assert claims["iss"] == "issuer"


@pytest.mark.unit
def test_build_assertion_contract_examples_include_required_surface() -> None:
    example = build_assertion_contract_examples("https://issuer.example/token")[0]
    assert example["grant_type"] == JWT_BEARER_GRANT_TYPE
    assert "assertion" in example
    assert "client_assertion" in example


@pytest.mark.unit
def test_validate_jwt_assertion_disabled() -> None:
    token = encode_jwt(
        iss="issuer",
        sub="subject",
        aud="https://issuer.example/token",
        exp=int(time.time()) + 60,
    )
    with patch.object(settings, "enable_rfc7521", False):
        with pytest.raises(RuntimeError):
            validate_jwt_assertion(token, audience="https://issuer.example/token")
