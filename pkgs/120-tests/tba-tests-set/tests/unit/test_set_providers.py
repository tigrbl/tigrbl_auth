from datetime import datetime, timezone

import pytest
from tba_contracts_identity.security_events import (
    SecurityEvent,
    SecurityEventSubject,
)
from tba_provider_replay_memory import MemoryReplayCheckProvider
from tba_provider_set_receiver import SetReceiverProvider, VerifiedSetToken
from tba_provider_set_transmitter import SetTransmitterProvider

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
        MemoryReplayCheckProvider(),
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
        MemoryReplayCheckProvider(),
        "https://issuer.example",
        "https://receiver.example",
    )
    with pytest.raises(ValueError):
        receiver.receive("header.payload.signature")


def test_replay_key_is_issuer_and_jti_not_jti_alone():
    store = MemoryReplayCheckProvider()
    claims = {
        "iss": "https://issuer-a.example",
        "aud": "https://receiver.example",
        "iat": 1,
        "jti": "same",
        "events": {EVENT_TYPE: {}},
    }

    def receiver(issuer):
        return SetReceiverProvider(
            lambda value, profile: VerifiedSetToken(
                {"typ": "secevent+jwt"}, {**claims, "iss": issuer}, profile
            ),
            store,
            issuer,
            "https://receiver.example",
        )

    first = receiver("https://issuer-a.example")
    assert (
        first.receive("header.payload.signature").issuer == "https://issuer-a.example"
    )
    assert (
        receiver("https://issuer-b.example").receive("header.payload.signature").issuer
        == "https://issuer-b.example"
    )
    with pytest.raises(ValueError, match="replay"):
        first.receive("header.payload.signature")
