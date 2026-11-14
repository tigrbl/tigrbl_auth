import pytest
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ec
from tba_concrete_certificate_x509 import parse_x509_certificate
from tba_profile_workload_credential_wimse_wic import validate_wic
from tba_profile_workload_credential_wimse_wit import verify_wit
from tba_profile_workload_proof_wimse_wpt import authenticate_wpt_request
from tba_protocol_workload_wimse_identifier import WorkloadIdentifier
from tba_testkit_workload_credential_conformance.fixtures import (
    AUDIENCE,
    WIMSE,
    Replay,
    _certificate,
    _jwk,
    _jwt,
    _wpt,
)


@pytest.mark.parametrize(
    "invalid",
    [
        "wimse://user@example.org/w",
        "wimse://example.org:1/w",
        "wimse://example.org/w?",
        "spiffe://example.org/w",
        "wimse://example.org/w/../other",
        "wimse://example.org/w/%2e%2E/other",
    ],
)
def test_native_identifier_contract(invalid):
    assert (
        str(WorkloadIdentifier.parse("WIMSE://EXAMPLE.ORG/workload/%7e"))
        == WIMSE + "/~"
    )
    with pytest.raises(ValueError):
        WorkloadIdentifier.parse(invalid)


def test_wimse_signed_wit_and_http_proof():
    issuer = ec.generate_private_key(ec.SECP256R1())
    workload = ec.generate_private_key(ec.SECP256R1())
    wit = _jwt(
        issuer,
        {"sub": WIMSE, "exp": 200, "cnf": {"jwk": _jwk(workload)}},
        typ="wit+jwt",
        kid="wit",
    )
    trust = {"example.org": [_jwk(issuer, kid="wit")]}
    replay = Replay()
    assert verify_wit(wit, trust_by_domain=trust, now=100).claims["sub"] == WIMSE
    headers = [
        ("Workload-Identity-Token", wit),
        ("Authorization", "WPT " + _wpt(workload, wit)),
    ]
    assert (
        authenticate_wpt_request(
            headers,
            audience=AUDIENCE,
            trust_by_domain=trust,
            now=100,
            replay_store=replay,
        ).claims["sub"]
        == WIMSE
    )
    with pytest.raises(ValueError, match="replay"):
        authenticate_wpt_request(
            headers,
            audience=AUDIENCE,
            trust_by_domain=trust,
            now=100,
            replay_store=replay,
        )
    with pytest.raises(ValueError, match="signature"):
        authenticate_wpt_request(
            headers[:1] + [("Authorization", "WPT " + _wpt(issuer, wit))],
            audience=AUDIENCE,
            trust_by_domain=trust,
            now=100,
            replay_store=Replay(),
        )


def test_wit_issuer_rotation_and_validity():
    old = ec.generate_private_key(ec.SECP256R1())
    new = ec.generate_private_key(ec.SECP256R1())
    workload = ec.generate_private_key(ec.SECP256R1())
    claims = {"sub": WIMSE, "exp": 200, "cnf": {"jwk": _jwk(workload)}}
    old_wit = _jwt(old, claims, typ="wit+jwt", kid="old")
    new_wit = _jwt(new, claims, typ="wit+jwt", kid="new")
    trust = {"example.org": [_jwk(old, kid="old"), _jwk(new, kid="new")]}
    assert verify_wit(old_wit, trust_by_domain=trust, now=100).claims["sub"] == WIMSE
    assert verify_wit(new_wit, trust_by_domain=trust, now=100).claims["sub"] == WIMSE
    trust["example.org"] = [_jwk(new, kid="new")]
    with pytest.raises(ValueError, match="signing key"):
        verify_wit(old_wit, trust_by_domain=trust, now=100)
    with pytest.raises(ValueError, match="validity"):
        verify_wit(new_wit, trust_by_domain=trust, now=200)


def test_shared_wimse_identifier_in_signed_token_and_certificate():
    issuer = ec.generate_private_key(ec.SECP256R1())
    certificate, _ = _certificate(
        ("wimse://EXAMPLE.ORG/workload",), issuer=_certificate(())
    )
    wic = validate_wic(
        parse_x509_certificate(certificate.public_bytes(serialization.Encoding.DER))
    )
    wit = _jwt(
        issuer, {"sub": WIMSE, "exp": 200, "cnf": {"jwk": _jwk(issuer)}}, typ="wit+jwt"
    )
    verified = verify_wit(wit, trust_by_domain={"example.org": [_jwk(issuer)]}, now=100)
    assert verified.jwt.integrity_verified
    assert (
        str(WorkloadIdentifier.parse(verified.claims["sub"])) == wic.workload_identifier
    )
