import pytest
from tba_protocol_cwt.profile import CwtProfile
from tba_protocol_jwt.profile import JwtProfile
from tba_protocol_security_cose import COSEProfile
from tba_protocol_security_jwe import JWEProfile
from tba_protocol_security_jws import JWSProfile


def test_each_envelope_standard_has_an_exact_version_owner() -> None:
    from tba_protocol_security_cose import CURRENT_VERSION as cose
    from tba_protocol_security_jwe import CURRENT_VERSION as jwe
    from tba_protocol_security_jws import CURRENT_VERSION as jws
    assert (jws.identifier, jwe.identifier, cose.identifier) == ("RFC7515", "RFC7516", "RFC9052")


def test_jwt_profiles_reject_type_and_algorithm_confusion() -> None:
    profile = JwtProfile("id-token", frozenset({"JWT"}), frozenset({"iss", "sub", "aud"}), frozenset({"RS256"}))
    profile.validate({"typ": "JWT", "alg": "RS256"}, {"iss": "i", "sub": "s", "aud": "a"})
    with pytest.raises(ValueError): profile.validate({"typ": "at+jwt", "alg": "RS256"}, {"iss": "i", "sub": "s", "aud": "a"})
    with pytest.raises(ValueError): profile.validate({"typ": "JWT", "alg": "none"}, {"iss": "i", "sub": "s", "aud": "a"})


def test_cwt_and_cose_profiles_enforce_labels_and_headers() -> None:
    CwtProfile("workload", frozenset({1, 2, 4}), frozenset({"Sign1"})).validate({1: "i", 2: "s", 4: 1}, "Sign1")
    with pytest.raises(ValueError): CwtProfile("workload", frozenset({1, 2, 4}), frozenset({"Sign1"})).validate({1: "i"}, "Sign1")
    COSEProfile("signed", frozenset({"ES256"}), frozenset({"alg"})).validate_headers({"alg": "ES256"})
    JWSProfile("signed", frozenset({"RS256"}), frozenset({"alg"})).validate_headers({"alg": "RS256"})
    JWEProfile("encrypted", frozenset({"RSA-OAEP"}), frozenset({"alg"})).validate_headers({"alg": "RSA-OAEP"})