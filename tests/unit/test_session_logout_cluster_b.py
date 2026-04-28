from __future__ import annotations

import asyncio
from types import SimpleNamespace
from uuid import uuid4

import pytest

from tigrbl_auth.standards.oidc import rp_initiated_logout as rp_logout
from tigrbl_auth.standards.oidc.session_mgmt import (
    compute_session_state,
    describe as describe_session_management,
    validate_session_state,
    validate_session_state_for_client,
)



def test_session_state_validation_accepts_matching_client_origin_and_salt() -> None:
    session_id = uuid4()
    presented = compute_session_state(
        client_id='client',
        redirect_uri='https://rp.example/callback',
        session_id=session_id,
        salt='salt-a',
    )
    result = validate_session_state(
        presented_session_state=presented,
        client_id='client',
        redirect_uri='https://rp.example/callback',
        session_id=session_id,
    )
    assert result.valid is True
    assert result.reason == 'validated'



def test_session_state_validation_rejects_origin_mismatch() -> None:
    session_id = uuid4()
    presented = compute_session_state(
        client_id='client',
        redirect_uri='https://rp.example/callback',
        session_id=session_id,
        salt='salt-a',
    )
    result = validate_session_state(
        presented_session_state=presented,
        client_id='client',
        redirect_uri='https://other.example/callback',
        session_id=session_id,
    )
    assert result.valid is False
    assert result.reason == 'hash_mismatch'



def test_validate_session_state_for_client_uses_session_salt() -> None:
    session_id = uuid4()
    session_row = SimpleNamespace(id=session_id, session_state_salt='salt-z')
    presented = compute_session_state(
        client_id='client',
        redirect_uri='https://rp.example/callback',
        session_id=session_id,
        salt='salt-z',
    )
    result = validate_session_state_for_client(
        session_row,
        presented_session_state=presented,
        client_id='client',
        redirect_uri='https://rp.example/callback',
    )
    assert result.valid is True



def test_session_management_description_is_truthful_about_iframe_claims() -> None:
    description = describe_session_management()
    assert description['session_state_validation_supported'] is True
    assert description['check_session_iframe_claimed'] is False
    assert description['auth_code_linkage_supported'] is True



def test_validate_post_logout_redirect_uri_accepts_registered_uri(monkeypatch: pytest.MonkeyPatch) -> None:
    client_id = uuid4()

    class _Registration:
        registration_metadata = {'post_logout_redirect_uris': ['https://rp.example/logout/callback']}

    class _Persistence:
        async def get_client_registration_async(self, resolved_client_id):
            assert resolved_client_id == client_id
            return _Registration()

    monkeypatch.setattr(rp_logout, '_persistence', lambda: _Persistence())
    validated = asyncio.run(
        rp_logout.validate_post_logout_redirect_uri(
            client_id=client_id,
            post_logout_redirect_uri='https://rp.example/logout/callback',
        )
    )
    assert validated == 'https://rp.example/logout/callback'



def test_validate_id_token_hint_rejects_sid_mismatch(monkeypatch: pytest.MonkeyPatch) -> None:
    session_id = uuid4()
    client_id = uuid4()

    async def _fake_verify(token: str, *, issuer: str, audience: str):
        assert token == 'hint-token'
        assert audience == str(client_id)
        return {'iss': issuer, 'aud': [str(client_id)], 'sid': str(uuid4()), 'sub': 'user-1'}

    monkeypatch.setattr(rp_logout, '_verify_id_token_hint', _fake_verify)
    with pytest.raises(rp_logout.HTTPException) as exc_info:
        asyncio.run(
            rp_logout.validate_id_token_hint(
                id_token_hint='hint-token',
                client_id=client_id,
                session_id=session_id,
                issuer='https://issuer.example',
            )
        )
    assert exc_info.value.status_code == 400
    assert exc_info.value.detail['error'] == 'invalid_id_token_hint'



def test_validate_logout_request_rejects_cross_client_misuse(monkeypatch: pytest.MonkeyPatch) -> None:
    session_client_id = uuid4()
    hinted_client_id = uuid4()
    session_row = SimpleNamespace(id=uuid4(), client_id=session_client_id, session_state='active', ended_at=None)

    async def _fake_verify(token: str, *, issuer: str, audience: str):
        return {'iss': issuer, 'aud': [str(hinted_client_id)], 'sid': str(session_row.id), 'sub': 'user-1'}

    monkeypatch.setattr(rp_logout, '_verify_id_token_hint', _fake_verify)
    with pytest.raises(rp_logout.HTTPException) as exc_info:
        asyncio.run(
            rp_logout.validate_logout_request(
                requested_client_id=session_client_id,
                post_logout_redirect_uri=None,
                id_token_hint='hint-token',
                session_row=session_row,
                issuer='https://issuer.example',
            )
        )
    assert exc_info.value.status_code == 400
    assert exc_info.value.detail['error'] == 'invalid_id_token_hint'



def test_build_logout_plan_reuses_existing_record_and_marks_replay(monkeypatch: pytest.MonkeyPatch) -> None:
    session_row = SimpleNamespace(id=uuid4(), user_id=uuid4())
    existing = SimpleNamespace(id=uuid4(), logout_metadata={'state': 'one'}, frontchannel_required=False, backchannel_required=False)

    class _Persistence:
        async def get_latest_logout_for_session_async(self, session_id):
            assert session_id == session_row.id
            return existing

        async def update_logout_metadata_async(self, logout_id, *, metadata=None, status=None):
            assert logout_id == existing.id
            existing.logout_metadata = dict(metadata or {})
            return existing

    monkeypatch.setattr(rp_logout, '_persistence', lambda: _Persistence())
    result = asyncio.run(
        rp_logout.build_logout_plan(
            session_row=session_row,
            client_id=None,
            post_logout_redirect_uri='https://rp.example/logout/callback',
            state='two',
            metadata={'id_token_hint_present': True},
        )
    )
    assert result is existing
    assert result.logout_metadata['replay_count'] == 1
    assert result.logout_metadata['post_logout_redirect_uri'] == 'https://rp.example/logout/callback'
    assert result.logout_metadata['id_token_hint_present'] is True
