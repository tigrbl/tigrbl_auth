import asyncio
from uuid import uuid4

import pytest

from tigrbl_auth_protocol_oidc.standards import backchannel_logout


class _Registration:
    registration_metadata = {
        "backchannel_logout_uri": "https://rp.example/backchannel",
        "backchannel_logout_session_required": True,
    }


class _Persistence:
    replay_keys = set()

    async def get_client_registration_async(self, client_id):
        return _Registration()

    async def register_backchannel_replay_async(self, *, jti, issuer, client_id, **_):
        key = (jti, issuer, client_id)
        if key in self.replay_keys:
            raise ValueError("logout token replay detected")
        self.replay_keys.add(key)


def test_backchannel_descriptor_and_logout_token_validation(monkeypatch):
    _Persistence.replay_keys.clear()
    persistence = _Persistence()
    descriptor = asyncio.run(
        backchannel_logout.build_backchannel_descriptor(
            client_id=uuid4(),
            sid="sid-1",
            sub="user-1",
            iss="https://issuer.example",
            logout_id=uuid4(),
            registration_metadata=_Registration.registration_metadata,
        )
    )
    assert descriptor["delivery"]["status"] == "pending"
    claims = asyncio.run(
        backchannel_logout.validate_backchannel_logout_token(
            descriptor["logout_token"],
            client_id=descriptor["client_id"],
            issuer="https://issuer.example",
            register_replay=persistence.register_backchannel_replay_async,
        )
    )
    assert claims["events"]
    with pytest.raises(ValueError):
        asyncio.run(
            backchannel_logout.validate_backchannel_logout_token(
                descriptor["logout_token"],
                client_id=descriptor["client_id"],
                issuer="https://issuer.example",
                register_replay=persistence.register_backchannel_replay_async,
            )
        )
