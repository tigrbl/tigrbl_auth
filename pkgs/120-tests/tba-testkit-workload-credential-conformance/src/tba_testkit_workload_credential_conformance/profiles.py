def exercise_wimse():
    from tba_profile_workload_credential_wimse_wit import validate_wit
    from tba_profile_workload_proof_wimse_wpt import validate_wpt

    wit_header = {"typ": "wit+jwt", "alg": "ES256"}
    wit = {
        "iss": "https://example.org/issuer",
        "sub": "wimse://example.org/workload",
        "cnf": {"jkt": "test-key-thumbprint"},
        "exp": 2,
        "iat": 1,
    }
    validate_wit(wit_header, wit)
    try:
        validate_wit(wit_header, {**wit, "aud": "service"})
    except ValueError as error:
        assert "aud" in str(error)
    else:
        raise AssertionError("WIT profile accepted an audience")

    wpt_header = {"typ": "wpt+jwt", "alg": "ES256"}
    wpt = {"aud": "service", "exp": 2, "jti": "proof", "wth": "expected-hash"}
    validate_wpt(
        wpt_header, wpt, expected_audience="service", expected_wit_hash="expected-hash"
    )
    try:
        validate_wpt(
            wpt_header, wpt, expected_audience="service", expected_wit_hash="wrong-hash"
        )
    except ValueError as error:
        assert "bind" in str(error)
    else:
        raise AssertionError("WPT profile accepted a mismatched WIT hash")


def exercise_wic():
    from datetime import datetime, timedelta, timezone

    from cryptography import x509
    from cryptography.hazmat.primitives import hashes, serialization
    from cryptography.hazmat.primitives.asymmetric import ec
    from cryptography.x509.oid import NameOID
    from tba_concrete_certificate_x509 import parse_x509_certificate
    from tba_profile_workload_credential_wimse_wic import validate_wic

    key = ec.generate_private_key(ec.SECP256R1())
    name = x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, "Fixture")])
    now = datetime.now(timezone.utc)
    identity = "wimse://example.org/workload"
    cert = (
        x509.CertificateBuilder()
        .subject_name(name)
        .issuer_name(name)
        .public_key(key.public_key())
        .serial_number(1)
        .not_valid_before(now)
        .not_valid_after(now + timedelta(minutes=1))
        .add_extension(
            x509.SubjectAlternativeName([x509.UniformResourceIdentifier(identity)]),
            False,
        )
        .sign(key, hashes.SHA256())
    )
    parsed = parse_x509_certificate(cert.public_bytes(serialization.Encoding.DER))
    assert validate_wic(parsed).workload_identifier == identity


def exercise_spiffe():
    from tba_protocol_workload_spiffe_svid import (
        validate_jwt_svid,
        validate_spiffe_id,
        validate_x509_svid,
    )

    subject = "spiffe://example.org/workload"
    assert validate_spiffe_id(subject) == ("example.org", "/workload")
    header = {"alg": "ES256"}
    jwt_svid = {"sub": subject, "aud": ["service"], "exp": 2, "iat": 1}
    validate_jwt_svid(header, jwt_svid, expected_audience="service")
    try:
        validate_jwt_svid(header, jwt_svid, expected_audience="other-service")
    except ValueError as error:
        assert "audience" in str(error)
    else:
        raise AssertionError("JWT-SVID profile accepted a different audience")

    options = {
        "dns_sans": (),
        "key_usage_digital_signature": True,
        "basic_constraints_ca": False,
    }
    assert validate_x509_svid(uri_sans=(subject,), **options) == subject
    try:
        validate_x509_svid(uri_sans=("wimse://example.org/workload",), **options)
    except ValueError:
        pass
    else:
        raise AssertionError("X.509-SVID profile accepted a WIMSE identifier")
