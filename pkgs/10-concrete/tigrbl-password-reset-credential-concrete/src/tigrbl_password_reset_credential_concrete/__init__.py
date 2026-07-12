from dataclasses import dataclass, field
from tigrbl_identity_contracts.credentials import CredentialKind
from tigrbl_identity_model_bases import CredentialBase, new_model_id


@dataclass(frozen=True, slots=True, kw_only=True)
class PasswordResetCredential(CredentialBase):
    id: str = field(default_factory=new_model_id)
    kind: CredentialKind = field(default=CredentialKind.PASSWORD_RESET, init=False)


__all__ = ["PasswordResetCredential"]
