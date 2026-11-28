"""Standalone X.509-SVID credential object."""

from dataclasses import dataclass, field
from tba_concrete_certificate_x509 import parse_x509_certificate
from tba_concrete_svid import SvidIdentity, normalize_spiffe_id
from tba_contracts_workload_identity import SvidFormat
from tba_bases_digital_credential import CredentialFormatBase


@dataclass(frozen=True, slots=True)
class X509SvidCredential(CredentialFormatBase):
    format_identifier = "x509-svid"
    spiffe_id: str
    certificate_chain: tuple[bytes, ...]
    key_reference: str | None = None
    bundle_reference: str | None = None
    hint: str | None = None
    identity: SvidIdentity = field(init=False)

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "identity",
            SvidIdentity(normalize_spiffe_id(self.spiffe_id), SvidFormat.X509),
        )
        if not self.spiffe_id.startswith("spiffe://"):
            raise ValueError("X.509-SVID requires a SPIFFE ID")
        object.__setattr__(self, "certificate_chain", tuple(self.certificate_chain))
        if not self.certificate_chain or any(
            not item for item in self.certificate_chain
        ):
            raise ValueError("X.509-SVID certificate chain is required")

    @property
    def certificate(self):
        certificate = parse_x509_certificate(self.certificate_chain[0])
        if certificate.uri_sans != (str(self.identity.spiffe_id),):
            raise ValueError("X.509-SVID certificate identity mismatch")
        return certificate


__all__ = ["X509SvidCredential"]
