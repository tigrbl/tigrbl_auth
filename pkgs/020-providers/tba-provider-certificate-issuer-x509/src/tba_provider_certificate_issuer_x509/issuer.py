"""CSR-based X.509 leaf issuance with an explicitly configured CA."""

from collections.abc import Callable
from datetime import datetime, timedelta, timezone
from ipaddress import ip_address

from cryptography import x509
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec, ed25519, ed448, rsa
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat
from cryptography.x509.oid import ExtensionOID, NameOID

from tba_bases_certificate import CertificateServiceBase
from tba_contracts_security_trust import (
    Artifact,
    CapabilityMap,
    CertificateRequest,
    IssueRequest,
)

from .config import X509IssuerConfig

_FORMATS = {"x509-pem": Encoding.PEM, "x509-der": Encoding.DER}
_SAN_TYPES = {
    "dns": x509.DNSName,
    "uri": x509.UniformResourceIdentifier,
    "email": x509.RFC822Name,
}
_NAME_OIDS = {
    "common_name": NameOID.COMMON_NAME,
    "organization_name": NameOID.ORGANIZATION_NAME,
}
_MANAGED_EXTENSIONS = {
    ExtensionOID.BASIC_CONSTRAINTS,
    ExtensionOID.SUBJECT_ALTERNATIVE_NAME,
    ExtensionOID.AUTHORITY_KEY_IDENTIFIER,
    ExtensionOID.SUBJECT_KEY_IDENTIFIER,
}


class InvalidCertificateRequest(ValueError):
    """A CSR or requested leaf profile cannot be issued."""


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


def _load_csr(value: bytes | Artifact | None) -> x509.CertificateSigningRequest:
    if isinstance(value, Artifact):
        value = value.bytes_value or (value.text_value or "").encode("utf-8")
    if not isinstance(value, bytes) or not value:
        raise InvalidCertificateRequest("a signed CSR is required")
    try:
        loader = (
            x509.load_pem_x509_csr
            if value.lstrip().startswith(b"-----BEGIN ")
            else x509.load_der_x509_csr
        )
        csr = loader(value)
        if not csr.is_signature_valid:
            raise InvalidCertificateRequest("invalid CSR signature")
    except (ValueError, TypeError) as exc:
        raise InvalidCertificateRequest("invalid signed CSR") from exc
    return csr


class X509CertificateIssuer(CertificateServiceBase):
    """Issue leaf certificates from signed CSRs and caller-approved attributes."""

    def __init__(
        self,
        config: X509IssuerConfig,
        *,
        clock: Callable[[], datetime] = _utcnow,
    ) -> None:
        ca, key = config.certificate, config.private_key
        if (
            type(config.max_lifetime_seconds) is not int
            or config.max_lifetime_seconds <= 0
        ):
            raise ValueError("maximum certificate lifetime must be a positive integer")
        if not isinstance(
            key,
            (
                rsa.RSAPrivateKey,
                ec.EllipticCurvePrivateKey,
                ed25519.Ed25519PrivateKey,
                ed448.Ed448PrivateKey,
            ),
        ):
            raise ValueError("unsupported CA signing key")
        public_format = (Encoding.DER, PublicFormat.SubjectPublicKeyInfo)
        if key.public_key().public_bytes(
            *public_format
        ) != ca.public_key().public_bytes(*public_format):
            raise ValueError("CA certificate does not match its signing key")
        if not ca.extensions.get_extension_for_class(x509.BasicConstraints).value.ca:
            raise ValueError("issuer certificate must be a CA")
        try:
            usage = ca.extensions.get_extension_for_class(x509.KeyUsage).value
        except x509.ExtensionNotFound:
            usage = None
        if usage is not None and not usage.key_cert_sign:
            raise ValueError("CA certificate does not permit certificate signing")
        self._config = config
        self._clock = clock

    def supports(self) -> CapabilityMap:
        return CapabilityMap(ops={"issue_certificate": ()}, formats=tuple(_FORMATS))

    async def issue(self, request: IssueRequest) -> Artifact:
        if request.op != "issue_certificate" or not isinstance(
            request.payload, CertificateRequest
        ):
            raise InvalidCertificateRequest(
                "certificate issuance requires a CertificateRequest payload"
            )
        return await self.issue_certificate(request.payload)

    async def issue_certificate(self, request: CertificateRequest) -> Artifact:
        if request.op != "issue_certificate" or any(
            value is not None
            for value in (
                request.key,
                request.issuer,
                request.issuer_cert,
                request.sig_alg,
            )
        ):
            raise InvalidCertificateRequest(
                "issuance requires the configured CA and a signed CSR"
            )
        output_format = "x509-der" if request.output_der else request.format
        if output_format not in _FORMATS:
            raise InvalidCertificateRequest("unsupported certificate output format")

        csr = _load_csr(request.csr)
        ca = self._config.certificate
        now = self._clock().astimezone(timezone.utc).replace(microsecond=0)
        if not ca.not_valid_before_utc <= now < ca.not_valid_after_utc:
            raise RuntimeError("CA certificate is outside its validity period")
        try:
            start = (
                now
                if request.not_before is None
                else datetime.fromtimestamp(request.not_before, timezone.utc)
            )
            stop = start + timedelta(seconds=self._config.max_lifetime_seconds)
            end = (
                min(stop, ca.not_valid_after_utc)
                if request.not_after is None
                else datetime.fromtimestamp(request.not_after, timezone.utc)
            )
            if (
                not ca.not_valid_before_utc
                <= start
                < end
                <= min(stop, ca.not_valid_after_utc)
            ):
                raise ValueError("requested validity exceeds CA policy")
            if end <= now or end > now + timedelta(
                seconds=self._config.max_lifetime_seconds
            ):
                raise ValueError("requested validity is outside the issuance window")

            subject = x509.Name(
                [
                    x509.NameAttribute(
                        _NAME_OIDS[name]
                        if name in _NAME_OIDS
                        else x509.ObjectIdentifier(name),
                        value,
                    )
                    for name, value in request.subject.items()
                ]
            )
            names = []
            for kind, values in request.san.items():
                values = (values,) if isinstance(values, str) else values
                if kind == "ip":
                    names.extend(x509.IPAddress(ip_address(value)) for value in values)
                else:
                    names.extend(_SAN_TYPES[kind](value) for value in values)
            if not subject and not names:
                raise ValueError("certificate requires an approved subject or SAN")
            public_key = csr.public_key()
            builder = (
                x509.CertificateBuilder()
                .subject_name(subject)
                .issuer_name(ca.subject)
                .public_key(public_key)
                .serial_number(
                    x509.random_serial_number()
                    if request.serial is None
                    else request.serial
                )
                .not_valid_before(start)
                .not_valid_after(end)
                .add_extension(
                    x509.BasicConstraints(ca=False, path_length=None), critical=True
                )
                .add_extension(
                    x509.SubjectKeyIdentifier.from_public_key(public_key),
                    critical=False,
                )
            )
            try:
                issuer_ski = ca.extensions.get_extension_for_class(
                    x509.SubjectKeyIdentifier
                ).value
            except x509.ExtensionNotFound:
                authority = x509.AuthorityKeyIdentifier.from_issuer_public_key(
                    ca.public_key()
                )
            else:
                authority = (
                    x509.AuthorityKeyIdentifier.from_issuer_subject_key_identifier(
                        issuer_ski
                    )
                )
            builder = builder.add_extension(authority, critical=False)
            if names:
                builder = builder.add_extension(
                    x509.SubjectAlternativeName(names), critical=not subject
                )
            for oid, (extension, critical) in request.extensions.items():
                if (
                    extension.oid.dotted_string != oid
                    or extension.oid in _MANAGED_EXTENSIONS
                ):
                    raise ValueError("invalid or issuer-managed certificate extension")
                if isinstance(extension, x509.KeyUsage) and (
                    extension.key_cert_sign or extension.crl_sign
                ):
                    raise ValueError(
                        "leaf certificates cannot sign certificates or CRLs"
                    )
                builder = builder.add_extension(extension, critical=critical)
        except (AttributeError, KeyError, OverflowError, TypeError, ValueError) as exc:
            raise InvalidCertificateRequest(str(exc)) from exc

        key = self._config.private_key
        algorithm = (
            None
            if isinstance(key, (ed25519.Ed25519PrivateKey, ed448.Ed448PrivateKey))
            else hashes.SHA256()
        )
        try:
            certificate = builder.sign(key, algorithm)
        except (TypeError, ValueError) as exc:
            raise InvalidCertificateRequest(
                "certificate signing rejected the CSR public key"
            ) from exc
        return Artifact(
            kind="certificate",
            format=output_format,
            bytes_value=certificate.public_bytes(_FORMATS[output_format]),
        )
