from dataclasses import dataclass, field
from typing import Any, Mapping
from tba_contracts_identity.credentials import Credential, CredentialKind
from tba_bases_authentication_credential import CredentialBase
from tba_primitives_identity import clean_mapping, new_model_id, required_text


@dataclass(frozen=True, slots=True, kw_only=True)
class DpopKeyCredential(CredentialBase):
    id: str = field(default_factory=new_model_id)
    kind: CredentialKind = field(default=CredentialKind.DPOP_KEY, init=False)
    jwk_thumbprint: str
    public_jwk: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        thumb = required_text(self.jwk_thumbprint, "JWK thumbprint")
        object.__setattr__(self, "jwk_thumbprint", thumb)
        object.__setattr__(self, "public_id", self.public_id or thumb)
        object.__setattr__(
            self, "public_jwk", clean_mapping(self.public_jwk, "public_jwk")
        )
        object.__setattr__(
            self,
            "metadata",
            {**dict(self.metadata), "public_jwk": dict(self.public_jwk)},
        )
        CredentialBase.__post_init__(self)

    @property
    def confirmation_claim(self):
        return {"jkt": self.jwk_thumbprint}

    def to_credential(self):
        return Credential(
            id=self.id,
            principal_id=self.principal_id,
            kind=CredentialKind.DPOP_KEY,
            public_id=self.jwk_thumbprint,
            status=self.status,
            metadata=self.metadata,
        )


__all__ = ["DpopKeyCredential"]
