from dataclasses import dataclass, field
from tigrbl_identity_contracts.credentials import CredentialKind, CredentialStatus
from tigrbl_authentication_credential_bases import CredentialBase
from tigrbl_identity_core import required_text


@dataclass(frozen=True, slots=True, kw_only=True)
class ServiceCredential(CredentialBase):
    id: str = ""
    principal_id: str = ""
    kind: CredentialKind = field(default=CredentialKind.SERVICE_KEY, init=False)
    credential_id: str
    service_id: str
    label: str
    raw_key: str
    revoked: bool = False

    def __post_init__(self):
        cid = required_text(self.credential_id, "credential id")
        sid = required_text(self.service_id, "service id")
        object.__setattr__(self, "credential_id", cid)
        object.__setattr__(self, "service_id", sid)
        object.__setattr__(self, "id", self.id or cid)
        object.__setattr__(self, "principal_id", self.principal_id or sid)
        object.__setattr__(self, "public_id", self.public_id or cid)
        object.__setattr__(
            self,
            "secret_digest",
            self.secret_digest or f"raw:{required_text(self.raw_key, 'raw key')}",
        )
        object.__setattr__(
            self, "status", CredentialStatus.REVOKED if self.revoked else self.status
        )
        CredentialBase.__post_init__(self)


__all__ = ["ServiceCredential"]
