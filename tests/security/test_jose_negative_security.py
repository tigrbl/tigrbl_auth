import pytest

from tigrbl_auth.security.certification import CertificationError, validate_jwk_set


def test_jose_negative_security_t0_contract_exports_validator() -> None:
    assert callable(validate_jwk_set)


def test_jose_negative_security_t1_accepts_valid_rs256_jwks() -> None:
    validate_jwk_set({"keys": [{"kid": "rsa-1", "kty": "RSA", "alg": "RS256"}]})


@pytest.mark.parametrize(
    "jwks,match",
    [
        ({"keys": [{"kid": "none", "kty": "RSA", "alg": "none"}]}, "algorithm"),
        (
            {"keys": [{"kid": "a", "kty": "RSA", "alg": "RS256"}, {"kid": "a", "kty": "RSA", "alg": "RS256"}]},
            "duplicate",
        ),
        ({"keys": [{"kid": "confused", "kty": "oct", "alg": "RS256"}]}, "RSA"),
        ({"keys": [{"kid": "bad-curve", "kty": "EC", "alg": "ES256", "crv": "P-192"}]}, "curve"),
    ],
)
def test_jose_negative_security_t2_rejects_malformed_or_confused_jwks(
    jwks: dict[str, object],
    match: str,
) -> None:
    with pytest.raises(CertificationError, match=match):
        validate_jwk_set(jwks)
