from dataclasses import dataclass, field
from tigrbl_identity_contracts.credentials import CredentialKind, CredentialStatus
from tigrbl_authentication_credential_bases import CredentialBase
from tigrbl_identity_core import required_text


@dataclass(frozen=True, slots=True, kw_only=True)
class MfaFactor(CredentialBase):
    id: str = ""
    principal_id: str = ""
    kind: CredentialKind = field(default=CredentialKind.MFA_FACTOR, init=False)
    factor_id: str
    subject_id: str
    tenant_id: str
    method: str
    bound_credential_id: str | None = None
    revoked: bool = False

    def __post_init__(self):
        fid = required_text(self.factor_id, "factor id")
        sid = required_text(self.subject_id, "subject id")
        object.__setattr__(self, "factor_id", fid)
        object.__setattr__(self, "subject_id", sid)
        object.__setattr__(self, "id", self.id or fid)
        object.__setattr__(self, "principal_id", self.principal_id or sid)
        object.__setattr__(self, "public_id", self.public_id or fid)
        object.__setattr__(
            self, "status", CredentialStatus.REVOKED if self.revoked else self.status
        )
        object.__setattr__(
            self,
            "metadata",
            {
                **dict(self.metadata),
                "tenant_id": self.tenant_id,
                "method": self.method,
                "bound_credential_id": self.bound_credential_id,
            },
        )
        CredentialBase.__post_init__(self)


__all__ = ["MfaFactor"]
