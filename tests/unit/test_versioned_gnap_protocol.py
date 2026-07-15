import asyncio

import pytest

from tigrbl_auth_protocol_gnap import (
    CAPABILITY_REQUIREMENTS,
    CURRENT_VERSION,
    GnapProtocol,
    capability_report,
    compatibility,
    compose_gnap_subject_claim_set,
    migrate_request,
    parse_gnap_request,
    supports,
)
from tigrbl_claim_assertions_concrete import AssertionsClaim
from tigrbl_claim_subject_identifiers_concrete import SubjectIdentifiersClaim
from tigrbl_claim_updated_at_rfc3339_concrete import UpdatedAtRfc3339Claim
from tigrbl_grant_negotiation_capability import GrantNegotiationCapability
from tigrbl_identity_contracts.gnap import GrantNegotiationResult


def test_gnap_owns_rfc_9635_version_and_features() -> None:
    assert CURRENT_VERSION.identifier == "RFC9635"
    assert CURRENT_VERSION.status == "proposed-standard"
    assert supports("multiple-access-tokens")
    assert not supports("multiple-access-tokens", "draft-13")


def test_gnap_parses_single_or_multiple_access_token_requests() -> None:
    request = parse_gnap_request(
        {"access_token": {"access": ["read"]}, "client": "key-ref"}
    )
    assert request.access_token == ({"access": ["read"]},)
    assert request.client == "key-ref"

    subject_only = parse_gnap_request(
        {
            "subject": {"sub_id_formats": ["opaque"]},
            "client": "key-ref",
        }
    )
    assert subject_only.access_token == ()


def test_gnap_migration_is_explicit() -> None:
    migrated = migrate_request(
        {"access_token": {}, "client": "key-ref"}, source="draft-13"
    )
    assert migrated == {"access_token": {}, "client": "key-ref"}
    with pytest.raises(ValueError, match="unsupported GNAP migration"):
        migrate_request({}, source="RFC9635", target="draft-13")


def test_gnap_subject_fields_are_standalone_claims() -> None:
    claims = compose_gnap_subject_claim_set(
        SubjectIdentifiersClaim([{"format": "opaque", "id": "subject-1"}]),
        AssertionsClaim([{"format": "id_token", "value": "a.b.c"}]),
        UpdatedAtRfc3339Claim("2024-10-01T12:00:00Z"),
    )

    assert set(claims.as_mapping()) == {"sub_ids", "assertions", "updated_at"}
    with pytest.raises(ValueError):
        UpdatedAtRfc3339Claim("2024-10-01T12:00:00")


def test_gnap_protocol_delegates_to_grant_capability_and_maps_requirements() -> None:
    capability = GrantNegotiationCapability(
        lambda request: GrantNegotiationResult(
            "grant-1",
            "approved",
            ({"value": "access-token", "access": ["read"]},),
        )
    )
    response = asyncio.run(
        GnapProtocol(capability).grant(
            {
                "access_token": {"access": ["read"]},
                "client": "client-instance-1",
            }
        )
    )

    assert response == {"access_token": {"value": "access-token", "access": ["read"]}}
    assert compatibility("draft-13").migration_required
    assert {requirement.operation for requirement in CAPABILITY_REQUIREMENTS} == {
        "check_and_reserve",
        "continue_grant",
        "request_grant",
        "rotate_access_token",
        "validate",
    }
    assert capability_report()["required_capabilities"] == (
        "artifact.processing",
        "grant.negotiation",
        "security.replay-protection",
    )
