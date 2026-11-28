from __future__ import annotations

from uuid import uuid4

import pytest

from tba_protocol_oidc.standards import backchannel_logout, frontchannel_logout


@pytest.mark.asyncio
async def test_frontchannel_descriptor_and_validation(monkeypatch: pytest.MonkeyPatch) -> None:
    client_id = uuid4()

    class _Registration:
        registration_metadata = {
            "frontchannel_logout_uri": "https://rp.example/frontchannel-logout",
            "frontchannel_logout_session_required": True,
            "frontchannel_retry_window_seconds": 45,
        }

    class _Persistence:
        async def get_client_registration_async(self, resolved_client_id):
            assert resolved_client_id == client_id
            return _Registration()

    descriptor = await frontchannel_logout.build_frontchannel_descriptor(
        client_id=client_id,
        sid="sid-123",
        iss="https://issuer.example",
        logout_id=uuid4(),
        registration_metadata=_Registration.registration_metadata,
    )
    assert descriptor is not None
    assert descriptor["delivery"]["status"] == "pending"
    assert descriptor["delivery"]["replay_protected"] is True
    assert descriptor["delivery"]["retry_window_seconds"] == 45
    assert "sid=sid-123" in str(descriptor["redirect_uri"])
    validated = frontchannel_logout.validate_frontchannel_request(
        params={"iss": "https://issuer.example", "sid": "sid-123", "logout_id": descriptor["logout_id"]},
        expected_sid="sid-123",
        expected_iss="https://issuer.example",
        expected_logout_id=descriptor["logout_id"],
    )
    assert validated["logout_id"] == descriptor["logout_id"]


@pytest.mark.asyncio
async def test_backchannel_logout_token_fallback_and_replay(monkeypatch: pytest.MonkeyPatch) -> None:
    client_id = uuid4()
    logout_id = uuid4()
    seen_jti: set[str] = set()

    class _Registration:
        registration_metadata = {
            "backchannel_logout_uri": "https://rp.example/backchannel-logout",
            "backchannel_logout_session_required": True,
        }

    class _Persistence:
        async def get_client_registration_async(self, resolved_client_id):
            assert resolved_client_id == client_id
            return _Registration()

        async def register_backchannel_replay_async(
            self,
            *,
            jti: str,
            issuer: str,
            client_id: str,
            expires_at,
            now,
        ):
            assert issuer == "https://issuer.example"
            assert client_id
            assert expires_at > now
            if jti in seen_jti:
                raise ValueError("replayed logout token")
            seen_jti.add(jti)

    def _missing_jwt_coder_cls():
        raise RuntimeError("no runtime JWT coder in dependency-light checkpoint")

    persistence = _Persistence()
    monkeypatch.setattr(backchannel_logout, "_jwt_coder_cls", _missing_jwt_coder_cls)
    descriptor = await backchannel_logout.build_backchannel_descriptor(
        client_id=client_id,
        sid="sid-123",
        sub="user-123",
        iss="https://issuer.example",
        logout_id=logout_id,
        registration_metadata=_Registration.registration_metadata,
    )
    assert descriptor is not None
    assert descriptor["delivery"]["status"] == "pending"
    assert descriptor["delivery"]["replay_protected"] is True
    claims = await backchannel_logout.validate_backchannel_logout_token(
        str(descriptor["logout_token"]),
        client_id=client_id,
        issuer="https://issuer.example",
        register_replay=persistence.register_backchannel_replay_async,
    )
    assert claims["events"]
    assert claims["sid"] == "sid-123"
    with pytest.raises(ValueError):
        await backchannel_logout.validate_backchannel_logout_token(
            str(descriptor["logout_token"]),
            client_id=client_id,
            issuer="https://issuer.example",
            register_replay=persistence.register_backchannel_replay_async,
        )
