import json
import pytest
from tba_primitives_identity.base64url import base64url_encode
from tba_concrete_jwt import decode_jwt_unverified
from tba_concrete_oidc_id_token import OidcIdToken


def _jwt(claims, *, typ="JWT"):
    header = base64url_encode(
        json.dumps({"alg": "ES256", "typ": typ}, separators=(",", ":")).encode()
    )
    payload = base64url_encode(json.dumps(claims, separators=(",", ":")).encode())
    signature = base64url_encode(b"structural-signature")
    return decode_jwt_unverified(f"{header}.{payload}.{signature}")


def test_oidc_id_token_is_a_standalone_token_object() -> None:
    token = OidcIdToken(
        _jwt(
            {
                "iss": "https://issuer.example",
                "sub": "user",
                "aud": "client",
                "exp": 20,
                "iat": 10,
            },
            typ="JWT",
        )
    )
    assert token.claims["aud"] == "client"
    with pytest.raises(ValueError, match="required claims"):
        OidcIdToken(_jwt({"sub": "user"}))
