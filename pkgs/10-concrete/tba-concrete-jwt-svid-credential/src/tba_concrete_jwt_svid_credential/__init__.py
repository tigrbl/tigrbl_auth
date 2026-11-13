"""Standalone JWT-SVID credential object."""

from dataclasses import dataclass, field
from tba_concrete_svid import SvidIdentity, normalize_spiffe_id
from tba_contracts_workload_identity import SvidFormat
from tba_bases_digital_credential import CredentialFormatBase
from tba_concrete_jwt import JwtObject


@dataclass(frozen=True, slots=True)
class JwtSvidCredential(CredentialFormatBase):
    format_identifier = "jwt-svid"
    jwt: JwtObject
    spiffe_id: str
    audience: tuple[str, ...]
    identity: SvidIdentity = field(init=False)

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "identity",
            SvidIdentity(normalize_spiffe_id(self.spiffe_id), SvidFormat.JWT),
        )
        object.__setattr__(self, "audience", tuple(self.audience))
        if not self.spiffe_id.startswith("spiffe://"):
            raise ValueError("JWT-SVID requires a SPIFFE ID")
        if self.jwt.claims.get("sub") != self.spiffe_id:
            raise ValueError("JWT-SVID subject mismatch")
        if not self.audience:
            raise ValueError("JWT-SVID audience is required")


__all__ = ["JwtSvidCredential"]
