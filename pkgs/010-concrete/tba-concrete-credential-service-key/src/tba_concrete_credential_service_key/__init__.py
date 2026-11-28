from dataclasses import dataclass, field
from tba_contracts_identity.credentials import CredentialKind
from tba_bases_authentication_credential import CredentialBase
from tba_primitives_identity import new_model_id


@dataclass(frozen=True, slots=True, kw_only=True)
class ServiceKeyCredential(CredentialBase):
    id: str = field(default_factory=new_model_id)
    kind: CredentialKind = field(default=CredentialKind.SERVICE_KEY, init=False)


__all__ = ["ServiceKeyCredential"]
