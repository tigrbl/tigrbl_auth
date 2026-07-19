import pytest
from tigrbl_auth_protocol_oidc.id_token_profile import validate_id_token_profile
from tigrbl_oauth_profile_jwt_access_token import validate_access_token

def test_oidc_id_token_profile_enforces_nonce_azp_and_type() -> None:
    claims = {"iss": "https://issuer", "sub": "subject", "aud": ["client", "api"], "azp": "client", "exp": 200, "iat": 100, "nonce": "n"}
    validate_id_token_profile({"alg": "RS256", "typ": "JWT"}, claims, expected_issuer="https://issuer", client_id="client", expected_nonce="n", now=150)
    with pytest.raises(ValueError): validate_id_token_profile({"alg": "RS256", "typ": "at+jwt"}, claims, expected_issuer="https://issuer", client_id="client", now=150)

def test_rfc9068_profile_cannot_be_used_as_an_id_token() -> None:
    claims = {"iss": "https://issuer", "sub": "subject", "aud": "api", "exp": 200, "iat": 100, "jti": "j", "client_id": "client"}
    validate_access_token({"alg": "RS256", "typ": "at+jwt"}, claims, expected_issuer="https://issuer", expected_audience="api")
    with pytest.raises(ValueError): validate_access_token({"alg": "RS256", "typ": "JWT"}, claims, expected_issuer="https://issuer", expected_audience="api")