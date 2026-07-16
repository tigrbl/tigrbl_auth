from dataclasses import dataclass, field
from tigrbl_identity_contracts.credentials import CredentialKind, CredentialStatus
from tigrbl_authentication_credential_bases import CredentialBase
from tigrbl_identity_core import clean_tuple, required_text


@dataclass(frozen=True, slots=True, kw_only=True)
class PasswordlessCredential(CredentialBase):
    id: str = ""
    principal_id: str = ""
    kind: CredentialKind = field(default=CredentialKind.PASSWORD_RESET, init=False)
    credential_id: str
    subject_id: str
    tenant_id: str
    credential_kind: str
    recovery_codes: tuple[str, ...]
    revoked: bool = False

    def __post_init__(self) -> None:
        credential_id = required_text(self.credential_id, "credential id")
        subject_id = required_text(self.subject_id, "subject id")
        object.__setattr__(self, "credential_id", credential_id)
        object.__setattr__(self, "subject_id", subject_id)
        object.__setattr__(self, "id", self.id or credential_id)
        object.__setattr__(self, "principal_id", self.principal_id or subject_id)
        object.__setattr__(self, "public_id", self.public_id or credential_id)
        object.__setattr__(self, "recovery_codes", clean_tuple(self.recovery_codes))
        object.__setattr__(
            self, "status", CredentialStatus.REVOKED if self.revoked else self.status
        )
        object.__setattr__(
            self,
            "metadata",
            {
                **dict(self.metadata),
                "tenant_id": self.tenant_id,
                "credential_kind": self.credential_kind,
                "recovery_codes": list(self.recovery_codes),
            },
        )
        CredentialBase.__post_init__(self)


__all__ = ["PasswordlessCredential"]
