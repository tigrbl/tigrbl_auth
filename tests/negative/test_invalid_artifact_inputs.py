from __future__ import annotations

from datetime import datetime, timedelta, timezone
from types import SimpleNamespace

import pytest

from tigrbl_auth.standards.jose.rfc7516 import JWEPolicyError, decrypt_jwe
from tigrbl_auth.standards.oauth2.assertion_framework import JWT_BEARER_GRANT_TYPE, validate_assertion_grant_request
from tigrbl_auth.standards.oauth2.par import PushedAuthorizationRequestError, validate_pushed_authorization_request_row


@pytest.mark.negative
def test_invalid_compact_jwe_and_assertion_inputs_are_rejected() -> None:
    with pytest.raises(JWEPolicyError):
        __import__("asyncio").run(decrypt_jwe("not-a-valid-jwe", {"kty": "oct", "k": b"0" * 32}))
    with pytest.raises(ValueError):
        validate_assertion_grant_request({"grant_type": JWT_BEARER_GRANT_TYPE}, audience="https://issuer.example/token")


@pytest.mark.negative
def test_par_request_uri_rejects_expired_consumed_or_mismatched_rows() -> None:
    now = datetime.now(timezone.utc)
    expired = SimpleNamespace(request_uri="urn:ietf:params:oauth:request_uri:expired", expires_at=now - timedelta(seconds=1), consumed_at=None, client_id="client-a", params={})
    with pytest.raises(PushedAuthorizationRequestError):
        validate_pushed_authorization_request_row(expired, client_id="client-a")

    consumed = SimpleNamespace(request_uri="urn:ietf:params:oauth:request_uri:used", expires_at=now + timedelta(minutes=5), consumed_at=now, client_id="client-a", params={})
    with pytest.raises(PushedAuthorizationRequestError):
        validate_pushed_authorization_request_row(consumed, client_id="client-a")

    mismatched = SimpleNamespace(request_uri="urn:ietf:params:oauth:request_uri:ok", expires_at=now + timedelta(minutes=5), consumed_at=None, client_id="client-a", params={})
    with pytest.raises(PushedAuthorizationRequestError):
        validate_pushed_authorization_request_row(mismatched, client_id="client-b")
