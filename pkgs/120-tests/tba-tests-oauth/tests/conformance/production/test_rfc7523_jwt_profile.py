from __future__ import annotations

from tba_auth.rfc.rfc7523 import (
    JWT_BEARER_ASSERTION_TYPE,
    PRIVATE_KEY_JWT_AUTH_METHOD,
    authenticate_client_assertion,
    build_client_assertion_contract_examples,
    make_client_assertion_jwt,
    token_endpoint_auth_methods_supported,
    token_endpoint_auth_signing_alg_values_supported,
)


TOKEN_AUDIENCE = "https://issuer.example/token"


def test_rfc7523_client_assertion_contract_and_validation() -> None:
    token = make_client_assertion_jwt("client", TOKEN_AUDIENCE)
    claims = authenticate_client_assertion(
        client_assertion_type=JWT_BEARER_ASSERTION_TYPE,
        client_assertion=token,
        audience=TOKEN_AUDIENCE,
        client_id="client",
        token_endpoint_auth_method=PRIVATE_KEY_JWT_AUTH_METHOD,
    )
    assert claims["iss"] == "client"
    assert PRIVATE_KEY_JWT_AUTH_METHOD in token_endpoint_auth_methods_supported()
    assert token_endpoint_auth_signing_alg_values_supported() == ["EdDSA"]

    example = build_client_assertion_contract_examples(TOKEN_AUDIENCE)[0]
    assert example["client_assertion_type"] == JWT_BEARER_ASSERTION_TYPE
    assert example["token_endpoint_auth_method"] == PRIVATE_KEY_JWT_AUTH_METHOD
    assert example["audience"] == TOKEN_AUDIENCE
