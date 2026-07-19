"""Standalone VC secured with JOSE."""
from dataclasses import dataclass
from typing import Mapping
from tigrbl_digital_credential_bases import CredentialFormatBase
from tigrbl_jws_concrete import JwsCompact

@dataclass(frozen=True, slots=True)
class VcJoseCredential(CredentialFormatBase):
    format_identifier="vc-jose"
    envelope: JwsCompact
    credential_claims: Mapping[str, object]
    def __post_init__(self) -> None:
        if not self.credential_claims: raise ValueError("VC-JOSE credential claims are required")
        object.__setattr__(self,"credential_claims",dict(self.credential_claims))

__all__=["VcJoseCredential"]