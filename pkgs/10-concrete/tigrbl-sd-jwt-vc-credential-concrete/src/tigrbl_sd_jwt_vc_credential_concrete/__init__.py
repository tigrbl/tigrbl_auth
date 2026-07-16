from dataclasses import dataclass
from typing import Mapping

from tigrbl_digital_credential_bases import CredentialFormatBase
from tigrbl_sd_jwt_concrete import SdJwtSerialization


@dataclass(frozen=True, slots=True)
class SdJwtVcCredential(CredentialFormatBase):
    format_identifier = "dc+sd-jwt"
    serialization: SdJwtSerialization
    header: Mapping[str, object]
    claims: Mapping[str, object]

    @property
    def issuer_jwt(self) -> str:
        return self.serialization.issuer_jwt

    @property
    def disclosures(self) -> tuple[str, ...]:
        return self.serialization.disclosures

    @property
    def key_binding_jwt(self) -> str | None:
        return self.serialization.key_binding_jwt


__all__ = ["SdJwtVcCredential"]
