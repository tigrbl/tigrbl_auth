from __future__ import annotations

import time

from tba_auth import encode_jwt
from tba_auth.rfc.rfc7521 import (
    JWT_BEARER_ASSERTION_TYPE,
    JWT_BEARER_GRANT_TYPE,
    build_assertion_contract_examples,
    validate_assertion_grant_request,
)


TOKEN_AUDIENCE = "https://issuer.example/token"


def test_rfc7521_assertion_grant_examples_and_validation() -> None:
    token = encode_jwt(
        iss="issuer",
        sub="subject",
        aud=TOKEN_AUDIENCE,
        exp=int(time.time()) + 60,
        iat=int(time.time()),
    )
    claims = validate_assertion_grant_request(
        {"grant_type": JWT_BEARER_GRANT_TYPE, "assertion": token},
        audience=TOKEN_AUDIENCE,
    )
    assert claims["iss"] == "issuer"

    example = build_assertion_contract_examples(TOKEN_AUDIENCE)[0]
    assert example["grant_type"] == JWT_BEARER_GRANT_TYPE
    assert example["client_assertion_type"] == JWT_BEARER_ASSERTION_TYPE
    assert example["audience"] == TOKEN_AUDIENCE
