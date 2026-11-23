from __future__ import annotations

from typing import Any, Mapping
from urllib.parse import unquote

from cryptography import x509


def normalize_presented_pem(value: str | bytes | None) -> bytes | None:
    if value in {None, b"", ""}:
        return None
    text = value.decode("utf-8") if isinstance(value, bytes) else str(value)
    text = unquote(text).replace("\\n", "\n").strip()
    if not text.startswith("-----BEGIN CERTIFICATE-----"):
        return None
    return text.encode("utf-8")


def _cert_from_pem(cert_pem: str | bytes) -> x509.Certificate:
    pem = normalize_presented_pem(cert_pem) or (
        cert_pem if isinstance(cert_pem, bytes) else str(cert_pem).encode("utf-8")
    )
    return x509.load_pem_x509_certificate(pem)


def certificate_subject_dn(cert_pem: str | bytes) -> str:
    return _cert_from_pem(cert_pem).subject.rfc4514_string()


def certificate_san_values(cert_pem: str | bytes) -> dict[str, tuple[str, ...]]:
    cert = _cert_from_pem(cert_pem)
    try:
        sans = cert.extensions.get_extension_for_class(
            x509.SubjectAlternativeName
        ).value
    except x509.ExtensionNotFound:
        return {"dns": (), "uri": (), "ip": (), "email": ()}
    return {
        "dns": tuple(sans.get_values_for_type(x509.DNSName)),
        "uri": tuple(sans.get_values_for_type(x509.UniformResourceIdentifier)),
        "ip": tuple(str(value) for value in sans.get_values_for_type(x509.IPAddress)),
        "email": tuple(sans.get_values_for_type(x509.RFC822Name)),
    }


def _metadata_values(metadata: Mapping[str, Any], key: str) -> tuple[str, ...]:
    value = metadata.get(key)
    if value is None:
        return ()
    if isinstance(value, (list, tuple, set)):
        return tuple(str(item).strip() for item in value if str(item).strip())
    text = str(value).strip()
    return (text,) if text else ()


def registered_certificate_identity_metadata(
    registration_metadata: Mapping[str, Any] | None,
) -> dict[str, tuple[str, ...]]:
    metadata = dict(registration_metadata or {})
    return {
        "subject_dn": _metadata_values(metadata, "tls_client_auth_subject_dn"),
        "san_dns": _metadata_values(metadata, "tls_client_auth_san_dns"),
        "san_uri": _metadata_values(metadata, "tls_client_auth_san_uri"),
        "san_ip": _metadata_values(metadata, "tls_client_auth_san_ip"),
        "san_email": _metadata_values(metadata, "tls_client_auth_san_email"),
    }


def certificate_matches_registered_identity(
    cert_pem: str | bytes,
    registration_metadata: Mapping[str, Any] | None,
) -> bool:
    expected = registered_certificate_identity_metadata(registration_metadata)
    if not any(expected.values()):
        return False
    if expected["subject_dn"] and certificate_subject_dn(cert_pem) in set(
        expected["subject_dn"]
    ):
        return True
    sans = certificate_san_values(cert_pem)
    return any(
        set(expected[key]).intersection(sans[san_key])
        for key, san_key in (
            ("san_dns", "dns"),
            ("san_uri", "uri"),
            ("san_ip", "ip"),
            ("san_email", "email"),
        )
    )


__all__ = [
    "certificate_matches_registered_identity",
    "certificate_san_values",
    "certificate_subject_dn",
    "normalize_presented_pem",
    "registered_certificate_identity_metadata",
]
