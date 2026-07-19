"""Standalone SPIFFE WIT-SVID credential object."""
from dataclasses import dataclass
from tigrbl_digital_credential_bases import CredentialFormatBase
from tigrbl_wit_concrete import WorkloadIdentityToken

@dataclass(frozen=True, slots=True)
class WitSvidCredential(CredentialFormatBase):
    format_identifier="wit-svid"
    token: WorkloadIdentityToken
    spiffe_id: str
    confirmation_key_thumbprint: str|None=None
    def __post_init__(self) -> None:
        if not self.spiffe_id.startswith("spiffe://"): raise ValueError("WIT-SVID subject must be a SPIFFE ID")
        if self.token.claims.get("sub") != self.spiffe_id: raise ValueError("WIT-SVID subject mismatch")

__all__=["WitSvidCredential"]