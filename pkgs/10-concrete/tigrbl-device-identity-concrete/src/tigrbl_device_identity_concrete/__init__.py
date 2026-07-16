from dataclasses import dataclass, field
from tigrbl_identity_contracts.principals import PrincipalKind, PrincipalStatus
from tigrbl_identity_bases import IdentityBase
from tigrbl_identity_core import required_text


@dataclass(frozen=True, slots=True, kw_only=True)
class DeviceIdentity(IdentityBase):
    id: str = ""
    subject: str = ""
    kind: PrincipalKind = field(default=PrincipalKind.DEVICE_IDENTITY, init=False)
    device_id: str = ""
    subject_id: str = ""
    credential_posture: str = ""
    last_ip_country: str | None = None
    created_at: str = ""
    revoked: bool = False

    def __post_init__(self):
        did = required_text(self.device_id or self.id or self.subject, "device id")
        sid = required_text(self.subject_id or self.subject or did, "subject id")
        object.__setattr__(self, "device_id", did)
        object.__setattr__(self, "subject_id", sid)
        object.__setattr__(self, "id", self.id or did)
        object.__setattr__(self, "subject", self.subject or sid)
        if self.revoked:
            object.__setattr__(self, "status", PrincipalStatus.DISABLED)
        IdentityBase.__post_init__(self)


__all__ = ["DeviceIdentity"]
