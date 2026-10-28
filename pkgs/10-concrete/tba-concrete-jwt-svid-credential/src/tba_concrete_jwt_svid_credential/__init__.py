"""Standalone JWT-SVID credential object."""
from dataclasses import dataclass
from tba_bases_digital_credential import CredentialFormatBase
from tba_concrete_jwt import JwtObject

@dataclass(frozen=True, slots=True)
class JwtSvidCredential(CredentialFormatBase):
    format_identifier="jwt-svid"
    jwt: JwtObject
    spiffe_id: str
    audience: tuple[str, ...]
    def __post_init__(self)->None:
        object.__setattr__(self,"audience",tuple(self.audience))
        if not self.spiffe_id.startswith("spiffe://"): raise ValueError("JWT-SVID requires a SPIFFE ID")
        if self.jwt.claims.get("sub") != self.spiffe_id: raise ValueError("JWT-SVID subject mismatch")
        if not self.audience: raise ValueError("JWT-SVID audience is required")

__all__=["JwtSvidCredential"]