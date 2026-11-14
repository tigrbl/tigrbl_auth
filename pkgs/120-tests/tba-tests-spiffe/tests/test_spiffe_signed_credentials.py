import pytest
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ec
from tba_profile_workload_credential_spiffe_wit_svid import verify_wit_svid
from tba_protocol_workload_spiffe_svid import verify_jwt_svid, verify_x509_svid
from tba_testkit_workload_credential_conformance.fixtures import (
    AUDIENCE,
    SPIFFE,
    PathValidator,
    Replay,
    _certificate,
    _jwk,
    _jwt,
    _mutual_tls_peers,
    _wpt,
)


def test_spiffe_signed_certificate_and_jwt():
    root = _certificate(())
    cert, _ = _certificate((SPIFFE,), issuer=root)
    chain = (cert.public_bytes(serialization.Encoding.DER),)
    assert (
        verify_x509_svid(
            chain, validators_by_domain={"example.org": PathValidator(root[0])}
        )
        == SPIFFE
    )
    with pytest.raises(ValueError, match="path"):
        verify_x509_svid(
            chain,
            validators_by_domain={"example.org": PathValidator(_certificate(())[0])},
        )
    key = ec.generate_private_key(ec.SECP256R1())
    jwt = _jwt(
        key, {"sub": SPIFFE, "aud": ["service"], "iat": 80, "exp": 200}, kid="jwt"
    )
    keys = {"example.org": [_jwk(key, kid="jwt", use="jwt-svid")]}
    assert (
        verify_jwt_svid(jwt, expected_audience="service", keys_by_domain=keys, now=100)
        == SPIFFE
    )
    with pytest.raises(ValueError, match="audience"):
        verify_jwt_svid(jwt, expected_audience="other", keys_by_domain=keys, now=100)


def test_spiffe_signed_wit_svid_and_proof():
    issuer = ec.generate_private_key(ec.SECP256R1())
    workload = ec.generate_private_key(ec.SECP256R1())
    wit = _jwt(
        issuer,
        {"sub": SPIFFE, "exp": 200, "cnf": {"jwk": _jwk(workload)}},
        typ="wit+jwt",
        kid="svid",
    )
    keys = {"example.org": [_jwk(issuer, kid="svid", use="wit-svid")]}
    assert (
        verify_wit_svid(
            wit,
            _wpt(workload, wit),
            audience=AUDIENCE,
            keys_by_domain=keys,
            now=100,
            replay_store=Replay(),
        )
        == SPIFFE
    )
    with pytest.raises(ValueError, match="WIT binding"):
        verify_wit_svid(
            wit,
            _wpt(workload, wit + "x"),
            audience=AUDIENCE,
            keys_by_domain=keys,
            now=100,
            replay_store=Replay(),
        )


def test_shared_svid_identity_and_x509_carrier():
    from tba_concrete_jwt import decode_jwt_unverified
    from tba_concrete_jwt_svid_credential import JwtSvidCredential
    from tba_concrete_wit import WorkloadIdentityToken
    from tba_concrete_wit_svid_credential import WitSvidCredential
    from tba_concrete_x509_svid_credential import X509SvidCredential

    root = _certificate(())
    cert, key = _certificate((SPIFFE,), issuer=root)
    x509_svid = X509SvidCredential(
        SPIFFE, (cert.public_bytes(serialization.Encoding.DER),)
    )
    jwt = decode_jwt_unverified(
        _jwt(key, {"sub": SPIFFE, "aud": "service", "exp": 200})
    )
    jwt_svid = JwtSvidCredential(jwt, SPIFFE, ("service",))
    wit = decode_jwt_unverified(
        _jwt(key, {"sub": SPIFFE, "cnf": {"jwk": _jwk(key)}, "exp": 200})
    )
    wit_svid = WitSvidCredential(WorkloadIdentityToken(wit), SPIFFE)
    assert x509_svid.certificate.uri_sans == (SPIFFE,)
    assert (
        x509_svid.identity.spiffe_id
        == jwt_svid.identity.spiffe_id
        == wit_svid.identity.spiffe_id
    )
    assert (
        len({value.identity.format for value in (x509_svid, jwt_svid, wit_svid)}) == 3
    )
    with pytest.raises(ValueError, match="subject mismatch"):
        JwtSvidCredential(jwt, SPIFFE + "/other", ("service",))


def test_spiffe_jwt_key_rotation():
    old = ec.generate_private_key(ec.SECP256R1())
    new = ec.generate_private_key(ec.SECP256R1())
    claims = {"sub": SPIFFE, "aud": ["service"], "iat": 80, "exp": 200}
    tokens = [_jwt(key, claims, kid=kid) for key, kid in ((old, "old"), (new, "new"))]
    trust = {
        "example.org": [
            _jwk(old, kid="old", use="jwt-svid"),
            _jwk(new, kid="new", use="jwt-svid"),
        ]
    }
    for token in tokens:
        assert (
            verify_jwt_svid(
                token, expected_audience="service", keys_by_domain=trust, now=100
            )
            == SPIFFE
        )
    trust["example.org"].pop(0)
    with pytest.raises(ValueError, match="signing key"):
        verify_jwt_svid(
            tokens[0], expected_audience="service", keys_by_domain=trust, now=100
        )
    with pytest.raises(ValueError, match="expiry"):
        verify_jwt_svid(
            tokens[1], expected_audience="service", keys_by_domain=trust, now=200
        )


def test_installed_style_jwt_svid_authentication_gate():
    from wsgiref.util import setup_testing_defaults

    issuer = ec.generate_private_key(ec.SECP256R1())
    claims = {"sub": SPIFFE, "aud": ["service"], "exp": 200}
    token = _jwt(issuer, claims)
    trust = {"example.org": [_jwk(issuer, kid="issuer", use="jwt-svid")]}

    def application(environ, start_response):
        scheme, _, credential = environ.get("HTTP_AUTHORIZATION", "").partition(" ")
        try:
            if scheme != "Bearer":
                raise ValueError("missing bearer credential")
            subject = verify_jwt_svid(
                credential, expected_audience="service", keys_by_domain=trust, now=100
            )
        except ValueError:
            start_response("401 Unauthorized", [])
            return [b""]
        start_response("200 OK", [])
        return [subject.encode()]

    request = {}
    setup_testing_defaults(request)
    request["HTTP_AUTHORIZATION"] = "Bearer " + token
    statuses = []

    def start_response(status, headers):
        statuses.append(status)

    assert application(request, start_response) == [SPIFFE.encode()]
    trust["example.org"] = [
        _jwk(ec.generate_private_key(ec.SECP256R1()), kid="new", use="jwt-svid")
    ]
    assert application(request, start_response) == [b""]
    assert statuses == ["200 OK", "401 Unauthorized"]


def test_signed_wit_svid_replay():
    issuer = ec.generate_private_key(ec.SECP256R1())
    workload = ec.generate_private_key(ec.SECP256R1())
    wit = _jwt(
        issuer,
        {"sub": SPIFFE, "exp": 200, "cnf": {"jwk": _jwk(workload)}},
        typ="wit+jwt",
        kid="issuer",
    )
    options = dict(
        audience=AUDIENCE,
        keys_by_domain={"example.org": [_jwk(issuer, kid="issuer", use="wit-svid")]},
        now=100,
        replay_store=Replay(),
    )
    proof = _wpt(workload, wit)
    assert verify_wit_svid(wit, proof, **options) == SPIFFE
    with pytest.raises(ValueError, match="replay"):
        verify_wit_svid(wit, proof, **options)


@pytest.mark.parametrize("identity", [SPIFFE])
def test_peer_identity_from_real_mutual_tls(tmp_path, identity):
    ca, der, server_der = _mutual_tls_peers(tmp_path, identity)
    validators = {"example.org": PathValidator(ca)}
    assert verify_x509_svid((der,), validators_by_domain=validators) == SPIFFE
