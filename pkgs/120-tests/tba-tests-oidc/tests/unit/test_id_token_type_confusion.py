import pytest
from tba_protocol_oidc.id_token_profile import validate_id_token_profile


ID_TOKEN_CLAIMS = {
    "iss": "https://issuer.example",
    "sub": "subject",
    "aud": "client",
    "exp": 200,
    "iat": 100,
}


def test_id_token_profile_rejects_oauth_access_token_type() -> None:
    with pytest.raises(ValueError, match="unexpected ID Token type"):
        validate_id_token_profile(
            {"alg": "RS256", "typ": "at+jwt"},
            ID_TOKEN_CLAIMS,
            expected_issuer="https://issuer.example",
            client_id="client",
            now=150,
        )
