import pytest

from tigrbl_auth_protocol_oidc.standards import id_token
from tigrbl_identity_core.errors import InvalidTokenError


class _Service:
    async def verify(self, token, *, issuer, audience):
        return {
            "iss": issuer,
            "sub": "subject",
            "aud": audience,
            "exp": 200,
            "iat": 100,
            "nonce": "expected",
        }


@pytest.mark.asyncio
async def test_runtime_id_token_verification_applies_oidc_profile(monkeypatch) -> None:
    async def service():
        return _Service(), "kid"

    monkeypatch.setattr(id_token, "id_token_service", service)
    token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.e30.signature"
    claims = await id_token.verify_id_token(
        token,
        issuer="https://issuer.example",
        audience="client",
        nonce="expected",
        now=150,
    )
    assert claims["sub"] == "subject"
    with pytest.raises(InvalidTokenError, match="nonce mismatch"):
        await id_token.verify_id_token(
            token,
            issuer="https://issuer.example",
            audience="client",
            nonce="wrong",
            now=150,
        )


@pytest.mark.asyncio
async def test_runtime_id_token_verification_rejects_wrong_profile(monkeypatch) -> None:
    async def service():
        return _Service(), "kid"

    monkeypatch.setattr(id_token, "id_token_service", service)
    access_token = "eyJhbGciOiJSUzI1NiIsInR5cCI6ImF0K2p3dCJ9.e30.signature"
    with pytest.raises(InvalidTokenError, match="unexpected ID Token type"):
        await id_token.verify_id_token(
            access_token,
            issuer="https://issuer.example",
            audience="client",
            now=150,
        )
