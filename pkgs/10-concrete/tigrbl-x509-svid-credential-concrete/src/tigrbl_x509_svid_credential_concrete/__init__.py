"""Standalone X.509-SVID credential object."""
from dataclasses import dataclass
from tigrbl_digital_credential_bases import CredentialFormatBase

@dataclass(frozen=True, slots=True)
class X509SvidCredential(CredentialFormatBase):
    format_identifier="x509-svid"
    spiffe_id: str
    certificate_chain: tuple[bytes, ...]
    key_reference: str|None=None
    bundle_reference: str|None=None
    hint: str|None=None
    def __post_init__(self)->None:
        if not self.spiffe_id.startswith("spiffe://"): raise ValueError("X.509-SVID requires a SPIFFE ID")
        object.__setattr__(self,"certificate_chain",tuple(self.certificate_chain))
        if not self.certificate_chain or any(not item for item in self.certificate_chain): raise ValueError("X.509-SVID certificate chain is required")

__all__=["X509SvidCredential"]