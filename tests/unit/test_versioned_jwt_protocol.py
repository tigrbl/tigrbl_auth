from tigrbl_auth_protocol_jwt import (
    CURRENT_VERSION,
    JWT_VERSION,
    migrate_claims,
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
