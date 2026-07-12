from dataclasses import dataclass, field
from tigrbl_identity_contracts.credentials import CredentialKind
from tigrbl_identity_model_bases import CredentialBase, new_model_id, required_text


@dataclass(frozen=True, slots=True, kw_only=True)
class PasskeyCredential(CredentialBase):
    id: str = field(default_factory=new_model_id)
    kind: CredentialKind = field(default=CredentialKind.PASSKEY_WEBAUTHN, init=False)
    credential_id: str
    public_key: str
    sign_count: int = 0

    def __post_init__(self):
        cid = required_text(self.credential_id, "credential id")
        key = required_text(self.public_key, "public key")
        object.__setattr__(self, "credential_id", cid)
        object.__setattr__(self, "public_key", key)
        object.__setattr__(self, "public_id", self.public_id or cid)
        object.__setattr__(
            self,
            "metadata",
            {
                **dict(self.metadata),
                "credential_id": cid,
                "public_key": key,
                "sign_count": int(self.sign_count),
            },
        )
        CredentialBase.__post_init__(self)


__all__ = ["PasskeyCredential"]
