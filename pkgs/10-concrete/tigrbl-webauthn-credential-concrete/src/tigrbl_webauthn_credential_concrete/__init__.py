from dataclasses import dataclass, field
from tigrbl_identity_contracts.credentials import CredentialKind, CredentialStatus
from tigrbl_identity_model_bases import CredentialBase, clean_tuple, required_text


@dataclass(frozen=True, slots=True, kw_only=True)
class WebAuthnCredential(CredentialBase):
    id: str = ""
    principal_id: str = ""
    kind: CredentialKind = field(default=CredentialKind.PASSKEY_WEBAUTHN, init=False)
    credential_id: str
    subject_id: str
    tenant_id: str
    rp_id: str
    algorithm: str
    transports: tuple[str, ...]
    sign_count: int = 0
    revoked: bool = False

    def __post_init__(self):
        cid = required_text(self.credential_id, "credential id")
        sid = required_text(self.subject_id, "subject id")
        object.__setattr__(self, "credential_id", cid)
        object.__setattr__(self, "subject_id", sid)
        object.__setattr__(self, "id", self.id or cid)
        object.__setattr__(self, "principal_id", self.principal_id or sid)
        object.__setattr__(self, "public_id", self.public_id or cid)
        object.__setattr__(self, "transports", clean_tuple(self.transports))
        object.__setattr__(
            self, "status", CredentialStatus.REVOKED if self.revoked else self.status
        )
        object.__setattr__(
            self,
            "metadata",
            {
                **dict(self.metadata),
                "tenant_id": self.tenant_id,
                "rp_id": self.rp_id,
                "algorithm": self.algorithm,
                "transports": list(self.transports),
                "sign_count": int(self.sign_count),
            },
        )
        CredentialBase.__post_init__(self)


__all__ = ["WebAuthnCredential"]
