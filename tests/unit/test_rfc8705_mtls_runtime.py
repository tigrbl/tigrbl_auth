from __future__ import annotations

from datetime import datetime, timedelta, timezone
from ipaddress import ip_address
from types import SimpleNamespace

import pytest
from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.x509.oid import NameOID

from tigrbl_auth_protocol_oauth.standards.mutual_tls_client_authentication import (
    authenticate_mtls_client,
    certificate_matches_registered_identity,
    certificate_san_values,
    certificate_subject_dn,
    presented_certificate_pem,
    presented_certificate_thumbprint,
    presented_trusted_certificate_thumbprint,
    thumbprint_from_cert_pem,
)


def _generate_cert_pem() -> bytes:
    key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    subject = issuer = x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, "client.example")])
    cert = (
        x509.CertificateBuilder()
        .subject_name(subject)
        .issuer_name(issuer)
        .public_key(key.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(datetime.now(timezone.utc) - timedelta(minutes=1))
        .not_valid_after(datetime.now(timezone.utc) + timedelta(days=1))
        .add_extension(
            x509.SubjectAlternativeName(
                [
                    x509.DNSName("client.example"),
                    x509.UniformResourceIdentifier("spiffe://tenant/service"),
                    x509.RFC822Name("client@example.test"),
                    x509.IPAddress(ip_address("127.0.0.1")),
                ]
            ),
            critical=False,
        )
        .sign(key, hashes.SHA256())
    )
    return cert.public_bytes(serialization.Encoding.PEM)


def test_rfc8705_tls_client_auth_subject_and_san_metadata_match_certificate() -> None:
    cert_pem = _generate_cert_pem()
    subject_dn = certificate_subject_dn(cert_pem)
    sans = certificate_san_values(cert_pem)

    assert subject_dn == "CN=client.example"
    assert "client.example" in sans["dns"]
    assert certificate_matches_registered_identity(
        cert_pem,
        {"token_endpoint_auth_method": "tls_client_auth", "tls_client_auth_subject_dn": subject_dn},
    )
    assert certificate_matches_registered_identity(
        cert_pem,
        {"token_endpoint_auth_method": "tls_client_auth", "tls_client_auth_san_uri": "spiffe://tenant/service"},
    )


def test_rfc8705_tls_client_auth_uses_subject_metadata_without_thumbprint_pin() -> None:
    cert_pem = _generate_cert_pem()
    authn = authenticate_mtls_client(
        {"token_endpoint_auth_method": "tls_client_auth", "tls_client_auth_san_dns": "client.example"},
        None,
        presented_certificate_pem=cert_pem,
        enabled=True,
    )

    assert authn.cert_thumbprint == thumbprint_from_cert_pem(cert_pem)


def test_rfc8705_tls_client_auth_rejects_unregistered_subject_metadata() -> None:
    cert_pem = _generate_cert_pem()

    with pytest.raises(ValueError, match="identity is not registered"):
        authenticate_mtls_client(
            {"token_endpoint_auth_method": "tls_client_auth", "tls_client_auth_san_dns": "other.example"},
            None,
            presented_certificate_pem=cert_pem,
            enabled=True,
        )


def test_mtls_forwarded_certificate_headers_require_trust_marker() -> None:
    cert_pem = _generate_cert_pem()
    thumbprint = thumbprint_from_cert_pem(cert_pem)
    request = SimpleNamespace(headers={"X-Client-Cert": cert_pem.decode("utf-8")}, scope={})

    assert presented_certificate_thumbprint(request) == thumbprint
    assert presented_trusted_certificate_thumbprint(request) is None
    assert presented_certificate_pem(request) is None

    trusted = SimpleNamespace(
        headers={"X-Client-Cert": cert_pem.decode("utf-8")},
        scope={"mtls_trusted_proxy": True},
    )
    assert presented_trusted_certificate_thumbprint(trusted) == thumbprint
    assert thumbprint_from_cert_pem(presented_certificate_pem(trusted) or b"") == thumbprint
