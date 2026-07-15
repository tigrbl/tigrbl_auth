import asyncio
from uuid import uuid4

from tigrbl_auth_protocol_oidc.standards import frontchannel_logout


class _Registration:
    registration_metadata = {
        "frontchannel_logout_uri": "https://rp.example/frontchannel",
        "frontchannel_logout_session_required": True,
    }


def test_frontchannel_descriptor_includes_delivery_state(monkeypatch):
    descriptor = asyncio.run(
        frontchannel_logout.build_frontchannel_descriptor(
            client_id=uuid4(),
            sid="sid-1",
            iss="https://issuer.example",
            logout_id=uuid4(),
            registration_metadata=_Registration.registration_metadata,
        )
    )
    assert descriptor["delivery"]["status"] == "pending"
    assert descriptor["delivery"]["replay_protected"] is True
    assert frontchannel_logout.validate_frontchannel_request(
        params={"iss": descriptor["iss"], "sid": "sid-1", "logout_id": descriptor["logout_id"]},
        expected_sid="sid-1",
        expected_iss=descriptor["iss"],
        expected_logout_id=descriptor["logout_id"],
    )["sid"] == "sid-1"
