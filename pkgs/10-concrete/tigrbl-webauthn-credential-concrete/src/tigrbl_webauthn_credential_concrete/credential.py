from __future__ import annotations

from dataclasses import dataclass, field

from tigrbl_identity_contracts.credentials import CredentialKind, CredentialStatus
from tigrbl_authentication_credential_bases import CredentialBase
from tigrbl_identity_core import clean_tuple, required_text


@dataclass(frozen=True, slots=True, kw_only=True)
class WebAuthnCredential(CredentialBase):
    """Registered WebAuthn public-key credential, not a ceremony response."""

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
    credential_external_id: bytes = b""
    credential_public_key_cose: bytes = b""
    user_handle: bytes | None = None
    cose_algorithm: int | None = None
    aaguid: bytes | None = None
    attestation_format: str | None = None
    attestation_type: str | None = None
    attestation_trust_status: str | None = None
    discoverable: bool = False
    backup_eligible: bool = False
    backup_state: bool = False
    display_name: str | None = None

    def __post_init__(self) -> None:
        cid = required_text(self.credential_id, "credential id")
        sid = required_text(self.subject_id, "subject id")
        rp_id = required_text(self.rp_id, "relying party id")
        if self.sign_count < 0:
            raise ValueError("WebAuthn signature counter cannot be negative")
        if self.backup_state and not self.backup_eligible:
            raise ValueError("a backed-up credential must be backup eligible")
        if self.aaguid is not None and len(self.aaguid) != 16:
            raise ValueError("WebAuthn AAGUID must be exactly 16 bytes")
        object.__setattr__(self, "credential_id", cid)
        object.__setattr__(self, "subject_id", sid)
        object.__setattr__(self, "rp_id", rp_id)
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
                "rp_id": rp_id,
                "algorithm": self.algorithm,
                "cose_algorithm": self.cose_algorithm,
                "transports": list(self.transports),
                "sign_count": int(self.sign_count),
                "discoverable": self.discoverable,
                "backup_eligible": self.backup_eligible,
                "backup_state": self.backup_state,
                "aaguid": self.aaguid.hex() if self.aaguid is not None else None,
                "attestation_format": self.attestation_format,
                "attestation_type": self.attestation_type,
                "attestation_trust_status": self.attestation_trust_status,
            },
        )
        CredentialBase.__post_init__(self)


__all__ = ["WebAuthnCredential"]
