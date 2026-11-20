"""Standalone VC secured with COSE."""
from dataclasses import dataclass
from typing import Mapping
from tba_concrete_cose import CoseMessage
from tba_bases_digital_credential import CredentialFormatBase

@dataclass(frozen=True, slots=True)
class VcCoseCredential(CredentialFormatBase):
    format_identifier="vc-cose"
    envelope: CoseMessage
    credential_claims: Mapping[str|int, object]
    def __post_init__(self) -> None:
        if not self.credential_claims: raise ValueError("VC-COSE credential claims are required")
        object.__setattr__(self,"credential_claims",dict(self.credential_claims))

__all__=["VcCoseCredential"]