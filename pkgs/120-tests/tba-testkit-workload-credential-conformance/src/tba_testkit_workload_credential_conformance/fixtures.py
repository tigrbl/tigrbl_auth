import hashlib
import json
from types import SimpleNamespace

from cryptography import x509
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec, utils
from tba_primitives_identity import base64url_encode

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
    from datetime import datetime, timedelta, timezone

    from cryptography import x509
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.asymmetric import ec
    from cryptography.x509.oid import NameOID

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


def _tls_context(tmp_path, name, leaf, root, *, server):
    import ssl

    from cryptography.hazmat.primitives import serialization

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


def _mutual_tls_peers(tmp_path, identity):
    import ssl

    root = _certificate(())
    server_context = _tls_context(
        tmp_path,
        "server",
        _certificate(
            ("wimse://example.org/workload/server",),
            issuer=root,
            dns="service.example.org",
        ),
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
    return (
        root[0],
        server.getpeercert(binary_form=True),
        client.getpeercert(binary_form=True),
    )


def exercise_wimse_mtls_round_trip():
    from pathlib import Path
    from tempfile import TemporaryDirectory

    from cryptography import x509
    from cryptography.exceptions import InvalidSignature
    from tba_concrete_certificate_x509 import parse_x509_certificate
    from tba_contracts_security_trust import (
        CertificatePathValidationResult,
        CertificateStatus,
    )
    from tba_profile_workload_authentication_wimse_mtls import (
        TLSPeer,
        verify_wimse_peer,
    )
    from tba_provider_certificate_status import SnapshotCertificateStatusProvider

    identity = "wimse://example.org/workload"
    with TemporaryDirectory() as directory:
        ca, client_der, server_der = _mutual_tls_peers(Path(directory), identity)
    status = SnapshotCertificateStatusProvider()

    class DirectPath:
        def __init__(self, anchor):
            self.anchor = anchor

        def validate(self, request):
            leaf = x509.load_der_x509_certificate(request.leaf.der)
            try:
                leaf.verify_directly_issued_by(self.anchor)
            except (ValueError, TypeError, InvalidSignature):
                return CertificatePathValidationResult(False, request.leaf.profile)
            return CertificatePathValidationResult(True, request.leaf.profile)

    client = TLSPeer(parse_x509_certificate(client_der))
    server = TLSPeer(
        parse_x509_certificate(server_der), server_name="service.example.org"
    )
    anchors = {"example.org": DirectPath(ca)}
    for peer, expected in ((client, identity), (server, identity + "/server")):
        status.publish(peer.certificate.der, CertificateStatus.GOOD, "acceptance-ca")
        assert (
            verify_wimse_peer(
                peer,
                expected_identity=expected,
                validators_by_domain=anchors,
                status_provider=status,
            ).workload_identifier
            == expected
        )
    wrong_anchor = {"example.org": DirectPath(_certificate(())[0])}
    for expected, validators, reason in (
        (identity, {}, "no configured"),
        (identity, wrong_anchor, "path"),
        (identity + "/other", anchors, "unexpected"),
        (identity, anchors, "status"),
    ):
        if reason == "status":
            status.publish(client_der, CertificateStatus.REVOKED, "acceptance-ca")
        try:
            verify_wimse_peer(
                client,
                expected_identity=expected,
                validators_by_domain=validators,
                status_provider=status,
            )
        except ValueError as error:
            assert reason in str(error)
        else:
            raise AssertionError(f"mTLS verifier accepted the {reason} case")


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
