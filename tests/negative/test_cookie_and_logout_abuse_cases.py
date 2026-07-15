from __future__ import annotations

import asyncio
from types import SimpleNamespace
from uuid import uuid4

import pytest

from tigrbl_auth.standards.http.cookies import parse_session_cookie_value
from tigrbl_auth_protocol_oidc.standards import rp_initiated_logout as rp_logout



def test_invalid_cookie_payload_is_rejected():
    assert parse_session_cookie_value('not-a-valid-cookie') is None



def test_invalid_cookie_uuid_is_rejected():
    assert parse_session_cookie_value('v1.not-a-uuid.secret') is None



def test_logout_redirect_requires_client_registration(monkeypatch: pytest.MonkeyPatch):
    client_id = uuid4()

    class _Registration:
        registration_metadata = {'post_logout_redirect_uris': ['https://rp.example/logout/callback']}

    class _Persistence:
        async def get_client_registration_async(self, resolved_client_id):
            assert resolved_client_id == client_id
            return _Registration()

    with pytest.raises(rp_logout.HTTPException) as exc_info:
        asyncio.run(
            rp_logout.validate_post_logout_redirect_uri(
                client_id=client_id,
                post_logout_redirect_uri='https://rp.example/unregistered',
                registration_metadata=_Registration.registration_metadata,
            )
        )
    assert exc_info.value.status_code == 400
    assert exc_info.value.detail['error'] == 'invalid_request'



def test_logout_rejects_invalid_id_token_hint(monkeypatch: pytest.MonkeyPatch):
    client_id = uuid4()

    async def _fake_verify(token: str, *, issuer: str, audience: str):
        raise ValueError('bad token')

    monkeypatch.setattr(rp_logout, '_verify_id_token_hint', _fake_verify)
    with pytest.raises(rp_logout.HTTPException) as exc_info:
        asyncio.run(
            rp_logout.validate_id_token_hint(
                id_token_hint='broken',
                client_id=client_id,
                issuer='https://issuer.example',
            )
        )
    assert exc_info.value.status_code == 400
    assert exc_info.value.detail['error'] == 'invalid_id_token_hint'



def test_logout_rejects_expired_session_rows():
    session_row = SimpleNamespace(id=uuid4(), client_id=uuid4(), session_state='expired', ended_at='2026-03-24T00:00:00Z')
    with pytest.raises(rp_logout.HTTPException) as exc_info:
        asyncio.run(
            rp_logout.validate_logout_request(
                requested_client_id=session_row.client_id,
                post_logout_redirect_uri=None,
                id_token_hint=None,
                session_row=session_row,
                issuer='https://issuer.example',
            )
        )
    assert exc_info.value.status_code == 400
    assert exc_info.value.detail['error'] == 'expired_session'



def test_logout_rejects_cross_client_misuse_without_hint():
    session_row = SimpleNamespace(id=uuid4(), client_id=uuid4(), session_state='active', ended_at=None)
    with pytest.raises(rp_logout.HTTPException) as exc_info:
        asyncio.run(
            rp_logout.validate_logout_request(
                requested_client_id=uuid4(),
                post_logout_redirect_uri=None,
                id_token_hint=None,
                session_row=session_row,
                issuer='https://issuer.example',
            )
        )
    assert exc_info.value.status_code == 400
    assert exc_info.value.detail['error'] == 'invalid_client'
