"""Standalone SPIFFE WIT-SVID credential object."""

from dataclasses import dataclass, field
from tba_concrete_svid import SvidIdentity, normalize_spiffe_id
from tba_contracts_workload_identity import SvidFormat
from tba_bases_digital_credential import CredentialFormatBase
from tba_concrete_wit import WorkloadIdentityToken


@dataclass(frozen=True, slots=True)
class WitSvidCredential(CredentialFormatBase):
    format_identifier = "wit-svid"
    token: WorkloadIdentityToken
    spiffe_id: str
    confirmation_key_thumbprint: str | None = None
    identity: SvidIdentity = field(init=False)

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "identity",
            SvidIdentity(normalize_spiffe_id(self.spiffe_id), SvidFormat.WIT),
        )
        if not self.spiffe_id.startswith("spiffe://"):
            raise ValueError("WIT-SVID subject must be a SPIFFE ID")
        if self.token.claims.get("sub") != self.spiffe_id:
            raise ValueError("WIT-SVID subject mismatch")


__all__ = ["WitSvidCredential"]
