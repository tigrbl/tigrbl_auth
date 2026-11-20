"""Configuration for a local X.509 issuing CA."""

from dataclasses import dataclass, field

from cryptography import x509
from cryptography.hazmat.primitives import serialization


@dataclass(frozen=True, slots=True)
class X509IssuerConfig:
    certificate: x509.Certificate
    private_key: object = field(repr=False)
    max_lifetime_seconds: int = 86400

    @classmethod
    def from_pem(
        cls,
        certificate: bytes,
        private_key: bytes,
        *,
        password: bytes | None = None,
        max_lifetime_seconds: int = 86400,
    ) -> "X509IssuerConfig":
        return cls(
            x509.load_pem_x509_certificate(certificate),
            serialization.load_pem_private_key(private_key, password=password),
            max_lifetime_seconds,
        )
