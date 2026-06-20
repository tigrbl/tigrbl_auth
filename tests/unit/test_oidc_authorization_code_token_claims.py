from __future__ import annotations

import uuid
from datetime import datetime, timedelta, timezone
from types import SimpleNamespace

import pytest

from tigrbl.requests import Request
from tigrbl_auth.rfc.rfc7636_pkce import makeCodeChallenge, makeCodeVerifier
from tigrbl_identity_storage.tables.token_record import _endpoint as token_endpoint


@pytest.mark.unit
@pytest.mark.asyncio
async def test_authorization_code_exchange_mints_session_bound_id_token_claims(monkeypatch):
    client_id = uuid.uuid4()
    tenant_id = uuid.uuid4()
    user_id = uuid.uuid4()
    session_id = uuid.uuid4()
    code_id = uuid.uuid4()
    auth_time = datetime(2026, 6, 15, 12, 34, 56, tzinfo=timezone.utc)
    verifier = makeCodeVerifier()
    challenge = makeCodeChallenge(verifier)
    auth_code = SimpleNamespace(
        id=code_id,
        client_id=client_id,
        user_id=user_id,
        tenant_id=tenant_id,
        session_id=session_id,
        redirect_uri="https://client.example/callback",
        code_challenge=challenge,
        nonce="nonce-123",
        scope="email openid profile",
        expires_at=datetime.now(timezone.utc) + timedelta(minutes=10),
        claims=None,
    )
    auth_session = SimpleNamespace(id=session_id, auth_time=auth_time)
    client = SimpleNamespace(
        id=client_id,
        tenant_id=tenant_id,
        verify_secret=lambda _secret: True,
    )
    minted: dict[str, object] = {}

    async def fake_parse_request_form(_request):
        return (
            {
                "grant_type": "authorization_code",
                "client_id": str(client_id),
                "code": str(code_id),
                "redirect_uri": "https://client.example/callback",
                "code_verifier": verifier,
            },
            [],
        )

    async def fake_load_client(_db, _client_id):
        return client, None

    async def fake_read_handler_record(model, _db, row_id):
        if model is token_endpoint.AuthCode:
            assert row_id == code_id
            return auth_code
        if model is token_endpoint.AuthSession:
            assert row_id == session_id
            return auth_session
        raise AssertionError(f"unexpected model lookup: {model!r}")

    async def fake_issue_token_pair_records(*_args, **_kwargs):
        return "access-token", "refresh-token"

    async def fake_mint_id_token(**kwargs):
        minted.update(kwargs)
        return "id-token"

    async def fake_delete_handler_record(model, _db, row_id):
        assert model is token_endpoint.AuthCode
        assert row_id == code_id

    monkeypatch.setattr(token_endpoint, "_enforce_tls", lambda _request, _deployment: None)
    monkeypatch.setattr(token_endpoint, "_parse_request_form", fake_parse_request_form)
    monkeypatch.setattr(token_endpoint, "_load_client", fake_load_client)
    monkeypatch.setattr(token_endpoint, "_resource_selection", lambda _resources, _audience: None)
    monkeypatch.setattr(
        token_endpoint,
        "validate_sender_constraint",
        lambda *_args, **_kwargs: SimpleNamespace(
            token_type="bearer",
            cert_thumbprint=None,
            confirmation_claim=None,
            jkt=None,
        ),
    )
    monkeypatch.setattr(token_endpoint, "issue_token_pair_records", fake_issue_token_pair_records)
    monkeypatch.setattr(token_endpoint, "read_handler_record", fake_read_handler_record)
    monkeypatch.setattr(token_endpoint, "delete_handler_record", fake_delete_handler_record)
    monkeypatch.setattr(token_endpoint, "mint_id_token", fake_mint_id_token)

    request = Request(scope={"type": "http", "scheme": "https", "headers": []})
    response = await token_endpoint.token_request(request=request, db=object())

    assert response["id_token"] == "id-token"
    assert minted["issuer"] in {
        "https://authn.example.com",
        "https://issuer.example/tenants/test",
    }
    assert minted["sub"] == str(user_id)
    assert minted["aud"] == str(client_id)
    assert minted["nonce"] == "nonce-123"
    assert minted["tid"] == str(tenant_id)
    assert minted["sid"] == str(session_id)
    assert minted["auth_time"] == int(auth_time.timestamp())
    assert minted["typ"] == "id"
    assert minted["at_hash"] == token_endpoint.oidc_hash("access-token")
    assert "azp" not in minted
