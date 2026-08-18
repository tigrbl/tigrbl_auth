from datetime import datetime, timezone

import pytest

from tigrbl_rp_session_runtime import InMemoryRPSessionRepository, InMemoryRPTransactionRepository, RPSessionRuntime, RPTransactionRuntime
from tigrbl_auth_protocol_rp import RPError, verify_id_token


def test_login_transaction_is_expiring_and_consumed_once() -> None:
    runtime = RPTransactionRuntime(InMemoryRPTransactionRepository())
    transaction = runtime.begin(
        issuer="https://id.example",
        client_id="customer",
        redirect_uri="https://app.example/callback",
        scope=("openid",),
        now=datetime(2026, 1, 1, tzinfo=timezone.utc),
    )
    assert runtime.consume(transaction.state, now=datetime(2026, 1, 1, tzinfo=timezone.utc)) == transaction
    with pytest.raises(ValueError, match="consumed"):
        runtime.consume(transaction.state, now=datetime(2026, 1, 1, tzinfo=timezone.utc))


def test_verified_token_requires_signature_claims_and_userinfo_subject() -> None:
    claims = {
        "iss": "https://id.example",
        "sub": "alice",
        "aud": "customer",
        "nonce": "nonce-1",
        "exp": 2_000_000_000,
        "iat": 1_900_000_000,
    }
    identity = verify_id_token(
        "signed-token",
        verifier=lambda token: claims if token == "signed-token" else {},
        issuer="https://id.example",
        audience="customer",
        nonce="nonce-1",
        now=1_950_000_000,
        userinfo={"sub": "alice", "email": "alice@example.com"},
    )
    assert identity.subject == "alice"
    with pytest.raises(RPError, match="UserInfo subject"):
        verify_id_token(
            "signed-token",
            verifier=lambda _: claims,
            issuer="https://id.example",
            audience="customer",
            nonce="nonce-1",
            now=1_950_000_000,
            userinfo={"sub": "mallory"},
        )


def test_refresh_tokens_are_encrypted_and_rotation_is_compare_and_swap() -> None:
    repository = InMemoryRPSessionRepository()
    runtime = RPSessionRuntime(repository, encrypt=lambda value: f"encrypted:{value}")
    expires = datetime(2026, 1, 2, tzinfo=timezone.utc)
    session = runtime.create(subject="alice", refresh_token="secret", expires_at=expires)
    assert session.encrypted_refresh_token == "encrypted:secret"
    rotated = runtime.rotate_refresh_token(session.session_id, expected_version=1, refresh_token="next", expires_at=expires)
    assert rotated.version == 2
    with pytest.raises(ValueError, match="concurrent"):
        runtime.rotate_refresh_token(session.session_id, expected_version=1, refresh_token="fork", expires_at=expires)
