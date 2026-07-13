import pytest

from tigrbl_audience_claim_concrete import AudienceClaim
from tigrbl_issued_at_claim_concrete import IssuedAtClaim
from tigrbl_issuer_claim_concrete import IssuerClaim
from tigrbl_jwt_id_claim_concrete import JwtIdClaim
from tigrbl_security_event_protocol_set import (
    CURRENT_VERSION,
    compose_set_claim_set,
    migrate_claims,
    supports,
)
from tigrbl_security_events_claim_concrete import SecurityEventsClaim


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
