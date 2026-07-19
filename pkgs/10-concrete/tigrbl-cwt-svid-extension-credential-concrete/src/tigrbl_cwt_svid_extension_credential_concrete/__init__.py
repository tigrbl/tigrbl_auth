"""Experimental Tigrbl CWT-SVID extension credential object."""
from dataclasses import dataclass
from typing import Mapping
from tigrbl_cwt_concrete import CwtClaimsSet
from tigrbl_digital_credential_bases import CredentialFormatBase

@dataclass(frozen=True, slots=True)
class CwtSvidExtensionCredential(CredentialFormatBase):
    format_identifier="cwt-svid-extension"
    encoded: bytes
    claims: CwtClaimsSet
    spiffe_id: str
    confirmation: Mapping[int|str, object]
    def __post_init__(self)->None:
        if not self.encoded: raise ValueError("CWT-SVID extension encoding is required")
        if not self.spiffe_id.startswith("spiffe://"): raise ValueError("CWT-SVID extension requires a SPIFFE ID")
        if self.claims.get_registered("sub") != self.spiffe_id: raise ValueError("CWT-SVID extension subject mismatch")
        if not self.confirmation: raise ValueError("CWT-SVID extension requires confirmation binding")
        object.__setattr__(self,"confirmation",dict(self.confirmation))

__all__=["CwtSvidExtensionCredential"]