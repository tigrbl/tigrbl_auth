from tigrbl_auth_protocol_oauth.standards.native_apps import (
    is_native_redirect_uri,
    validate_native_redirect_uri,
)


def test_rfc8252_native_redirect_validation_is_enforced():
    assert is_native_redirect_uri("com.example.app:/oauth2redirect") is True
    validate_native_redirect_uri("com.example.app:/oauth2redirect")
