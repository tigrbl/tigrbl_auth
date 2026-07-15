import pytest

from tigrbl_auth_protocol_jwt import (
    CURRENT_VERSION,
    JWT_CARRIER,
    JWT_VERSION,
    UnsupportedJwtMediaTypeError,
    capability_report,
    compatibility,
    migrate_claims,
    select_carrier,
    supports,
)


def test_jwt_owns_rfc_7519_history_and_feature_gates() -> None:
    assert CURRENT_VERSION.identifier == "RFC7519"
    assert JWT_VERSION == "RFC7519"
    assert supports("nested-jwt")
    assert not supports("nested-jwt", "draft-ietf-oauth-json-web-token-32")
    assert migrate_claims(
        {"sub": "subject"}, source="draft-ietf-oauth-json-web-token-32"
    ) == {"sub": "subject"}


def test_jwt_owns_compatibility_and_carrier_selection() -> None:
    path = compatibility("draft-ietf-oauth-json-web-token-32")

    assert path.compatible
    assert path.migration_required
    assert select_carrier("application/jwt") == JWT_CARRIER
    with pytest.raises(UnsupportedJwtMediaTypeError):
        select_carrier("application/cwt")


def test_jwt_maps_explicit_artifact_processing_capabilities() -> None:
    report = capability_report()

    assert report["required_capabilities"] == ("artifact.processing",)
    assert tuple(
        requirement.operation for requirement in report["requirements"]
    ) == ("decode", "validate", "encode")
