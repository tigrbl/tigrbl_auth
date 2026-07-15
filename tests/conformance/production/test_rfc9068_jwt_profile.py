from tigrbl_auth_protocol_oauth.standards.jwt_access_tokens import (
    add_jwt_access_token_claims,
    validate_jwt_access_token_claims,
)


def test_rfc9068_helpers_add_and_validate_profile_claims():
    payload = add_jwt_access_token_claims(
        {"sub": "user", "exp": 1},
        issuer="https://issuer.example",
        audience="https://resource.example",
    )
    validate_jwt_access_token_claims(
        payload, issuer="https://issuer.example", audience="https://resource.example"
    )
    assert payload["iss"] == "https://issuer.example"
    assert payload["aud"] == "https://resource.example"
