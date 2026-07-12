from dataclasses import dataclass, field
from tigrbl_identity_contracts.credentials import CredentialKind
from tigrbl_identity_model_bases import CredentialBase, new_model_id


@dataclass(frozen=True, slots=True, kw_only=True)
class ClientSecretCredential(CredentialBase):
    id: str = field(default_factory=new_model_id)
    kind: CredentialKind = field(default=CredentialKind.CLIENT_SECRET, init=False)


__all__ = ["ClientSecretCredential"]
