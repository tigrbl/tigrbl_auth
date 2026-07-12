from __future__ import annotations

import pytest

from tigrbl_set_concrete import (
    RFC8417_SPEC_URL,
    SET_TYP,
    SecurityEventTokenError,
    build_security_event_claims,
    event_data,
    validate_security_event_claims,
)

EVENT = "https://schemas.example/events/account-disabled"


def test_build_and_validate_set_claims() -> None:
    claims = build_security_event_claims(
        issuer="https://issuer.example",
        audience=["https://one.example", "https://two.example"],
        subject="user-123",
        events={EVENT: {"reason": "policy"}},
        issued_at=100,
        token_id="set-1",
        expires_at=200,
    )
    validated = validate_security_event_claims(
        claims,
        expected_issuer="https://issuer.example",
        expected_audience="https://two.example",
        now=150,
    )
    assert validated["sub"] == "user-123"
    assert event_data(claims, EVENT) == {"reason": "policy"}
    assert SET_TYP == "secevent+jwt"
    assert RFC8417_SPEC_URL.endswith("8417")


@pytest.mark.parametrize("missing", ["iss", "aud", "iat", "jti", "events"])
def test_required_claims(missing: str) -> None:
    claims = build_security_event_claims(
        issuer="https://issuer.example", audience="receiver", events={EVENT: {}}, issued_at=100
    )
    claims.pop(missing)
    with pytest.raises(SecurityEventTokenError, match="missing required"):
        validate_security_event_claims(claims, now=100)


def test_structured_sub_is_rejected() -> None:
    claims = build_security_event_claims(
        issuer="https://issuer.example", audience="receiver", events={EVENT: {}}, issued_at=100
    )
    claims["sub"] = {"format": "opaque", "id": "user-123"}
    with pytest.raises(SecurityEventTokenError, match="sub must be a string"):
        validate_security_event_claims(claims, now=100)


def test_empty_events_and_expired_token_are_rejected() -> None:
    with pytest.raises(SecurityEventTokenError, match="non-empty"):
        build_security_event_claims(issuer="https://issuer.example", audience="receiver", events={})
    claims = build_security_event_claims(
        issuer="https://issuer.example", audience="receiver", events={EVENT: {}}, issued_at=100, expires_at=101
    )
    with pytest.raises(SecurityEventTokenError, match="expired"):
        validate_security_event_claims(claims, now=101)
