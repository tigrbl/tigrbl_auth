import pytest

from tigrbl_claim_audience_concrete import AudienceClaim
from tigrbl_claim_issued_at_concrete import IssuedAtClaim
from tigrbl_claim_issuer_concrete import IssuerClaim
from tigrbl_claim_jwt_id_concrete import JwtIdClaim
from tigrbl_security_event_protocol_set import (
    CAPABILITY_REQUIREMENTS,
    CURRENT_VERSION,
    SET_JWT_CARRIER,
    UnsupportedSetMediaTypeError,
    capability_report,
    compatibility,
    compose_set_claim_set,
    migrate_claims,
    select_carrier,
    supports,
)
from tigrbl_claim_security_events_concrete import SecurityEventsClaim


def test_set_owns_rfc_8417_version_and_features() -> None:
    assert CURRENT_VERSION.identifier == "RFC8417"
    assert supports("non-token-use")
    assert not supports("non-token-use", "draft-ietf-secevent-token-13")


def test_set_composes_required_concrete_claim_objects() -> None:
    claims = compose_set_claim_set(
        IssuerClaim("https://issuer.example"),
        AudienceClaim("receiver"),
        IssuedAtClaim(1),
        JwtIdClaim("event-1"),
        SecurityEventsClaim({"https://schemas.example/event": {}}),
    )
    assert claims.version == "RFC8417"
    assert claims.get("events") is not None


def test_set_draft_migration_requires_events() -> None:
    assert migrate_claims({"events": {}}, source="draft-ietf-secevent-token-13") == {
        "events": {}
    }
    with pytest.raises(ValueError, match="requires the events claim"):
        migrate_claims({}, source="draft-ietf-secevent-token-13")


def test_set_owns_compatibility_carrier_and_explicit_delivery_bindings() -> None:
    path = compatibility("draft-ietf-secevent-token-13")
    assert path.compatible and path.migration_required
    assert select_carrier("application/secevent+jwt") is SET_JWT_CARRIER
    with pytest.raises(UnsupportedSetMediaTypeError):
        select_carrier("application/jwt")

    assert {item.operation for item in CAPABILITY_REQUIREMENTS} == {
        "check_and_reserve",
        "decode",
        "encode",
        "receive",
        "record_delivery",
        "record_event",
        "reserve_replay",
        "resolve_subscription",
        "transmit",
        "validate",
    }
    report = capability_report()
    assert report["required_capabilities"] == (
        "artifact.processing",
        "security-events.delivery",
        "security.replay-protection",
    )
