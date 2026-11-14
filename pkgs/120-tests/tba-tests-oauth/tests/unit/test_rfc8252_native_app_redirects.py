"""Dependency-light tests for RFC 8252 native app policy enforcement."""

from __future__ import annotations

import pytest

from tba_auth.rfc.rfc8252 import (
    RFC8252_SPEC_URL,
    classify_native_redirect_uri,
    is_native_redirect_uri,
    validate_native_authorization_request,
    validate_native_client_metadata,
    validate_native_redirect_uri,
    validate_native_token_request,
)


@pytest.mark.unit
def test_accepts_loopback_redirect_uri_with_explicit_port() -> None:
    assessment = validate_native_redirect_uri("http://127.0.0.1:49152/callback")
    assert assessment.kind == "loopback"
    assert assessment.port == 49152


@pytest.mark.unit
def test_accepts_private_use_scheme_redirect_uri_without_authority() -> None:
    assessment = validate_native_redirect_uri("com.example.app:/oauth2redirect")
    assert assessment.kind == "private-use-scheme"


@pytest.mark.unit
def test_rejects_public_http_redirect_uri() -> None:
    assert not is_native_redirect_uri("http://example.com/callback")
    with pytest.raises(ValueError):
        validate_native_redirect_uri("http://example.com/callback")


@pytest.mark.unit
def test_rejects_https_loopback_redirect_for_native_apps() -> None:
    with pytest.raises(ValueError):
        validate_native_redirect_uri("https://localhost:8443/callback")


@pytest.mark.unit
def test_rejects_private_use_scheme_with_authority() -> None:
    with pytest.raises(ValueError):
        validate_native_redirect_uri("com.example.app://oauth2redirect")


@pytest.mark.unit
def test_validate_native_client_metadata_derives_pkce_policy() -> None:
    metadata = validate_native_client_metadata(
        redirect_uris=["http://127.0.0.1:49152/callback", "com.example.app:/oauth2redirect"],
        response_types=["code"],
        grant_types=["authorization_code"],
    )
    assert metadata["native_application"] is True
    assert metadata["pkce_required"] is True
    assert sorted(metadata["redirect_uri_kinds"]) == ["loopback", "private-use-scheme"]


@pytest.mark.unit
def test_validate_native_client_metadata_rejects_non_code_response_type() -> None:
    with pytest.raises(ValueError):
        validate_native_client_metadata(
            redirect_uris=["http://127.0.0.1:49152/callback"],
            response_types=["token"],
            grant_types=["authorization_code"],
        )


@pytest.mark.unit
def test_validate_native_authorization_request_requires_pkce_and_code_flow() -> None:
    redirect_uri = "http://127.0.0.1:49152/callback"
    with pytest.raises(ValueError):
        validate_native_authorization_request(
            redirect_uri=redirect_uri,
            response_type="code",
            code_challenge=None,
            code_challenge_method="S256",
        )
    with pytest.raises(ValueError):
        validate_native_authorization_request(
            redirect_uri=redirect_uri,
            response_type="token",
            code_challenge="challenge",
            code_challenge_method="S256",
        )
    with pytest.raises(ValueError):
        validate_native_authorization_request(
            redirect_uri=redirect_uri,
            response_type="code",
            code_challenge="challenge",
            code_challenge_method="plain",
        )
    assessment = validate_native_authorization_request(
        redirect_uri=redirect_uri,
        response_type="code",
        code_challenge="challenge",
        code_challenge_method="S256",
    )
    assert assessment is not None and assessment.kind == "loopback"


@pytest.mark.unit
def test_validate_native_token_request_requires_code_verifier() -> None:
    redirect_uri = "http://127.0.0.1:49152/callback"
    with pytest.raises(ValueError):
        validate_native_token_request(redirect_uri=redirect_uri, code_verifier=None)
    validate_native_token_request(redirect_uri=redirect_uri, code_verifier="verifier")


@pytest.mark.unit
def test_classify_native_redirect_uri_records_profile_kind() -> None:
    assessment = classify_native_redirect_uri("com.example.app:/oauth2redirect")
    assert assessment is not None
    assert assessment.kind == "private-use-scheme"
    assert RFC8252_SPEC_URL.startswith("https://")
