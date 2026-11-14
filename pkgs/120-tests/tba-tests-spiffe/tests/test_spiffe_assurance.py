import json

from tba_testkit_workload_credential_conformance.wheels import run_installed

SPIFFE = ("tba-protocol-workload-spiffe-svid",)


def exercise_shared_svid():
    from tba_concrete_jwt import decode_jwt_unverified
    from tba_concrete_jwt_svid_credential import JwtSvidCredential
    from tba_concrete_svid import SvidIdentity
    from tba_concrete_x509_svid_credential import X509SvidCredential
    from tba_primitives_identity import base64url_encode

    subject = "spiffe://example.org/workload"
    jwt = decode_jwt_unverified(
        ".".join(
            base64url_encode(value)
            for value in (
                b'{"alg":"ES256"}',
                json.dumps({"sub": subject}).encode(),
                b"fixture",
            )
        )
    )
    assert isinstance(
        JwtSvidCredential(jwt, subject, ("service",)).identity, SvidIdentity
    )
    assert isinstance(X509SvidCredential(subject, (b"fixture",)).identity, SvidIdentity)


def exercise_optional_wit_svid():
    from tba_concrete_jwt import decode_jwt_unverified
    from tba_concrete_svid import SvidIdentity
    from tba_concrete_wit import WorkloadIdentityToken
    from tba_concrete_wit_svid_credential import WitSvidCredential
    from tba_primitives_identity import base64url_encode

    subject = "spiffe://example.org/workload"
    claims = {"sub": subject, "cnf": {"jwk": {}}, "exp": 100}
    jwt = decode_jwt_unverified(
        ".".join(
            base64url_encode(value)
            for value in (
                b'{"alg":"ES256"}',
                json.dumps(claims).encode(),
                b"fixture",
            )
        )
    )
    assert isinstance(
        WitSvidCredential(WorkloadIdentityToken(jwt), subject).identity, SvidIdentity
    )


def test_t2_shared_svid_compositions(wheelhouse, tmp_path, record_property):
    for label, packages, exercise, excluded in (
        ("standalone", SPIFFE, exercise_shared_svid, ("wimse", "spire")),
        (
            "optional-wit",
            ("tba-concrete-wit-svid-credential",),
            exercise_optional_wit_svid,
            ("spire",),
        ),
    ):
        directory = tmp_path / label
        directory.mkdir()
        inventory = run_installed(
            wheelhouse, directory, packages, (exercise,), excluded
        )
        record_property(
            label + "_wheel_inventory", json.dumps(inventory, sort_keys=True)
        )
