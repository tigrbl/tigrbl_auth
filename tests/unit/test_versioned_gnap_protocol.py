import pytest

from tigrbl_auth_protocol_gnap import (
    CURRENT_VERSION,
    migrate_request,
    parse_gnap_request,
    supports,
)


def test_gnap_owns_rfc_9635_version_and_features() -> None:
    assert CURRENT_VERSION.identifier == "RFC9635"
    assert CURRENT_VERSION.status == "standards-track"
    assert supports("multiple-access-tokens")
    assert not supports("multiple-access-tokens", "draft-13")


def test_gnap_parses_single_or_multiple_access_token_requests() -> None:
    request = parse_gnap_request(
        {"access_token": {"access": ["read"]}, "client": "key-ref"}
    )
    assert request.access_token == ({"access": ["read"]},)
    assert request.client == "key-ref"


def test_gnap_migration_is_explicit() -> None:
    migrated = migrate_request(
        {"access_token": {}, "client": "key-ref"}, source="draft-13"
    )
    assert migrated["_migration"] == {"from": "draft-13", "to": "RFC9635"}
    with pytest.raises(ValueError, match="unsupported GNAP migration"):
        migrate_request({}, source="RFC9635", target="draft-13")
