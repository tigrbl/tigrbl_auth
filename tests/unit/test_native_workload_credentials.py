"""Signed workload credentials and native WIC transport fixtures."""

import hashlib
import json
import ssl
from datetime import datetime, timedelta, timezone
from types import SimpleNamespace

import pytest
from cryptography import x509
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec, utils
from cryptography.x509.oid import NameOID
from tba_concrete_certificate_x509 import parse_x509_certificate
from tba_contracts_security_trust import CertificateStatus
from tba_primitives_identity import base64url_encode
from tba_profile_workload_authentication_wimse_mtls import TLSPeer, verify_wimse_peer
from tba_profile_workload_credential_spiffe_wit_svid import verify_wit_svid
from tba_profile_workload_credential_wimse_wic import validate_wic
from tba_profile_workload_credential_wimse_wit import verify_wit
from tba_profile_workload_proof_wimse_wpt import authenticate_wpt_request
from tba_protocol_workload_spiffe_svid import verify_jwt_svid, verify_x509_svid
from tba_protocol_workload_wimse_identifier import WorkloadIdentifier

WIMSE = "wimse://example.org/workload"
SPIFFE = "spiffe://example.org/workload"
AUDIENCE = "https://service.example.org/resource"


def _jwk(private_key, **metadata):
    numbers = private_key.public_key().public_numbers()
    return {
        "kty": "EC",
        "crv": "P-256",
        "alg": "ES256",
        "x": base64url_encode(numbers.x.to_bytes(32, "big")),
        "y": base64url_encode(numbers.y.to_bytes(32, "big")),
        **metadata,
    }


def _jwt(key, claims, **header):
    header = {"alg": "ES256", **header}
    segments = [
        base64url_encode(json.dumps(value).encode()) for value in (header, claims)
    ]
    message = ".".join(segments)
    r, s = utils.decode_dss_signature(
        key.sign(message.encode(), ec.ECDSA(hashes.SHA256()))
    )
    return (
        message + "." + base64url_encode(r.to_bytes(32, "big") + s.to_bytes(32, "big"))
    )


def _wpt(private, wit):
    return _jwt(
        private,
        {
            "aud": AUDIENCE,
            "exp": 120,
            "jti": "proof",
            "wth": base64url_encode(hashlib.sha256(wit.encode()).digest()),
        },
        typ="wpt+jwt",
    )


class Replay:
    def __init__(self):
        self.keys = set()

    def check_and_store(self, key, *, now, ttl_s):
        if key in self.keys:
            return False
        self.keys.add(key)
        return True


class PathValidator:
    def __init__(self, ca):
        self.ca = ca

    def validate(self, request):
        leaf = x509.load_der_x509_certificate(request.leaf.der)
        try:
            leaf.verify_directly_issued_by(self.ca)
        except (ValueError, TypeError, InvalidSignature):
            valid = False
        else:
            valid = True
        return SimpleNamespace(
            valid=valid, indeterminate=False, profile=request.leaf.profile
        )


class StatusProvider:
    def __init__(self, status):
        self._status = status

    def status(self, der):
        return SimpleNamespace(status=self._status)


def _certificate(subject, *, issuer=None, dns=None):
    now = datetime.now(timezone.utc)
    key = ec.generate_private_key(ec.SECP256R1())
    name = x509.Name(
        [
            x509.NameAttribute(
                NameOID.COMMON_NAME, "Workload CA" if issuer is None else "Workload"
            )
        ]
    )
    builder = (
        x509.CertificateBuilder()
        .subject_name(name)
        .issuer_name(issuer[0].subject if issuer else name)
        .public_key(key.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(now - timedelta(minutes=1))
        .not_valid_after(now + timedelta(hours=1))
        .add_extension(
            x509.BasicConstraints(ca=issuer is None, path_length=None), critical=True
        )
        .add_extension(
            x509.KeyUsage(
                digital_signature=True,
                content_commitment=False,
                key_encipherment=False,
                data_encipherment=False,
                key_agreement=False,
                key_cert_sign=issuer is None,
                crl_sign=issuer is None,
                encipher_only=False,
                decipher_only=False,
            ),
            critical=True,
        )
    )
    names = [x509.UniformResourceIdentifier(uri) for uri in subject]
    if dns:
        names.append(x509.DNSName(dns))
    if names:
        builder = builder.add_extension(
            x509.SubjectAlternativeName(names), critical=False
        )
    return builder.sign(issuer[1] if issuer else key, hashes.SHA256()), key


def test_certificate_and_wic_profile():
    root = _certificate(())
    cert, _ = _certificate((WIMSE,), issuer=root, dns="service.example.org")
    der = cert.public_bytes(serialization.Encoding.DER)
    parsed = parse_x509_certificate(cert.public_bytes(serialization.Encoding.PEM))
    assert parsed.der == der
    assert parsed.dns_sans == ("service.example.org",)
    assert parsed.key_usage.digital_signature
    assert validate_wic(parsed).workload_identifier == WIMSE
    invalid, _ = _certificate((WIMSE, WIMSE + "/other"), issuer=root)
    with pytest.raises(ValueError, match="exactly one"):
        validate_wic(
            parse_x509_certificate(invalid.public_bytes(serialization.Encoding.DER))
        )
    with pytest.raises(ValueError):
        parse_x509_certificate(b"invalid DER")


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


def _tls_context(tmp_path, name, leaf, root, *, server):
    certificate, key = leaf
    pem = tmp_path / f"{name}.pem"
    private_key = tmp_path / f"{name}.key"
    pem.write_bytes(certificate.public_bytes(serialization.Encoding.PEM))
    private_key.write_bytes(
        key.private_bytes(
            serialization.Encoding.PEM,
            serialization.PrivateFormat.PKCS8,
            serialization.NoEncryption(),
        )
    )
    context = ssl.SSLContext(
        ssl.PROTOCOL_TLS_SERVER if server else ssl.PROTOCOL_TLS_CLIENT
    )
    context.load_cert_chain(pem, private_key)
    context.load_verify_locations(
        cadata=root.public_bytes(serialization.Encoding.PEM).decode()
    )
    context.verify_mode = ssl.CERT_REQUIRED
    return context


@pytest.mark.parametrize("identity", [WIMSE, SPIFFE])
def test_peer_identity_from_real_mutual_tls(tmp_path, identity):
    root = _certificate(())
    server_context = _tls_context(
        tmp_path,
        "server",
        _certificate((WIMSE + "/server",), issuer=root, dns="service.example.org"),
        root[0],
        server=True,
    )
    client_context = _tls_context(
        tmp_path,
        "client",
        _certificate((identity,), issuer=root),
        root[0],
        server=False,
    )
    client_in, client_out = ssl.MemoryBIO(), ssl.MemoryBIO()
    server_in, server_out = ssl.MemoryBIO(), ssl.MemoryBIO()
    server = server_context.wrap_bio(server_in, server_out, server_side=True)
    client = client_context.wrap_bio(
        client_in, client_out, server_hostname="service.example.org"
    )
    complete = set()
    for _ in range(16):
        for endpoint, outgoing, remote in (
            (client, client_out, server_in),
            (server, server_out, client_in),
        ):
            if endpoint not in complete:
                try:
                    endpoint.do_handshake()
                except ssl.SSLWantReadError:
                    pass
                else:
                    complete.add(endpoint)
            if outgoing.pending:
                remote.write(outgoing.read())
        if len(complete) == 2:
            break
    assert len(complete) == 2
    der = server.getpeercert(binary_form=True)
    validators = {"example.org": PathValidator(root[0])}
    if identity == SPIFFE:
        assert verify_x509_svid((der,), validators_by_domain=validators) == SPIFFE
    else:
        peer = TLSPeer(parse_x509_certificate(der))
        assert (
            verify_wimse_peer(
                peer,
                expected_identity=WIMSE,
                validators_by_domain=validators,
                status_provider=StatusProvider(CertificateStatus.GOOD),
            ).workload_identifier
            == WIMSE
        )
        with pytest.raises(ValueError, match="status"):
            verify_wimse_peer(
                peer,
                expected_identity=WIMSE,
                validators_by_domain=validators,
                status_provider=StatusProvider(CertificateStatus.REVOKED),
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


def test_wic_peer_configuration_and_wrong_anchor():
    root = _certificate(())
    cert, _ = _certificate((WIMSE,), issuer=root, dns="service.example.org")
    peer = TLSPeer(
        parse_x509_certificate(cert.public_bytes(serialization.Encoding.DER)),
        server_name="service.example.org",
    )
    status = StatusProvider(CertificateStatus.GOOD)
    with pytest.raises(ValueError, match="no configured"):
        verify_wimse_peer(
            peer,
            expected_identity=WIMSE,
            validators_by_domain={},
            status_provider=status,
        )
    with pytest.raises(ValueError, match="path"):
        verify_wimse_peer(
            peer,
            expected_identity=WIMSE,
            validators_by_domain={"example.org": PathValidator(_certificate(())[0])},
            status_provider=status,
        )
    with pytest.raises(ValueError, match="unexpected"):
        verify_wimse_peer(
            peer,
            expected_identity=WIMSE + "/other",
            validators_by_domain={"example.org": PathValidator(root[0])},
            status_provider=status,
        )
    wrong_name = TLSPeer(peer.certificate, server_name="other.example.org")
    with pytest.raises(ValueError, match="server name"):
        verify_wimse_peer(
            wrong_name,
            expected_identity=WIMSE,
            validators_by_domain={"example.org": PathValidator(root[0])},
            status_provider=status,
        )


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
