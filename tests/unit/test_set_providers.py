from datetime import datetime, timezone

import pytest
from tigrbl_identity_contracts.security_events import (
    SecurityEvent,
    SecurityEventSubject,
)
from tigrbl_security_event_replay_store import InMemorySecurityEventReplayStore
from tigrbl_set_receiver_provider import SetReceiverProvider, VerifiedSetToken
from tigrbl_set_transmitter_provider import SetTransmitterProvider

EVENT_TYPE = "https://schemas.example/events/account-disabled"


def _event():
    return SecurityEvent(
        EVENT_TYPE,
        "https://issuer.example",
        ("https://receiver.example",),
        "event-1",
        datetime(2026, 1, 1, tzinfo=timezone.utc),
        SecurityEventSubject("sub", {"sub": "alice"}),
        {"reason": "policy"},
    )


def test_set_transmitter_uses_explicit_profile_typ_and_required_claims():
    captured = {}

    def signer(claims, header, profile):
        captured.update(claims=claims, header=header, profile=profile)
        return "header.payload.signature"

    token = SetTransmitterProvider(signer).transmit(
        _event(), "https://receiver.example"
    )
    assert token.count(".") == 2
    assert captured["header"]["typ"] == "secevent+jwt"
    assert captured["profile"] == "security-event-token"
    assert set(captured["claims"]) >= {"iss", "aud", "iat", "jti", "events"}


def test_set_receiver_verifies_profile_typ_claims_and_replay_once():
    captured = {}

    def signer(claims, header, profile):
        captured.update(claims=claims, header=header, profile=profile)
        return "header.payload.signature"

    token = SetTransmitterProvider(signer).transmit(
        _event(), "https://receiver.example"
    )
    receiver = SetReceiverProvider(
        lambda value, profile: VerifiedSetToken(
            captured["header"], captured["claims"], captured["profile"]
        ),
        InMemorySecurityEventReplayStore(),
        "https://issuer.example",
        "https://receiver.example",
    )
    event = receiver.receive(token)
    assert (
        event.event_type == EVENT_TYPE and event.subject.identifiers["sub"] == "alice"
    )
    with pytest.raises(ValueError, match="replay"):
        receiver.receive(token)


@pytest.mark.parametrize(
    ("typ", "profile"),
    [("JWT", "security-event-token"), ("secevent+jwt", "id-token")],
)
def test_set_receiver_rejects_id_access_or_untyped_jwt_profiles(typ, profile):
    claims = {
        "iss": "https://issuer.example",
        "aud": "https://receiver.example",
        "iat": 1,
        "jti": "event-1",
        "events": {EVENT_TYPE: {}},
    }
    receiver = SetReceiverProvider(
        lambda value, expected: VerifiedSetToken({"typ": typ}, claims, profile),
        InMemorySecurityEventReplayStore(),
        "https://issuer.example",
        "https://receiver.example",
    )
    with pytest.raises(ValueError):
        receiver.receive("header.payload.signature")


def test_replay_key_is_issuer_and_jti_not_jti_alone():
    store = InMemorySecurityEventReplayStore()
    assert store.consume_once("issuer-a", "same")
    assert store.consume_once("issuer-b", "same")
    assert not store.consume_once("issuer-a", "same")
