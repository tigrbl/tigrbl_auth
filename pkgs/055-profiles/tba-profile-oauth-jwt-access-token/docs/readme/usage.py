from tba_profile_oauth_jwt_access_token import validate_access_token

issuer = "https://issuer.example"
audience = "https://api.example"
validate_access_token(
    {"typ": "at+jwt", "alg": "ES256"},
    {
        "iss": issuer,
        "sub": "alice",
        "aud": audience,
        "exp": 1000,
        "iat": 900,
        "jti": "token-1",
        "client_id": "demo",
    },
    expected_issuer=issuer,
    expected_audience=audience,
)
