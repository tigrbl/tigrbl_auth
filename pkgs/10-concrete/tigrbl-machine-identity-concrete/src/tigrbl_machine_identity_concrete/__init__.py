from dataclasses import dataclass, field
from datetime import datetime
from tigrbl_identity_contracts.principals import PrincipalKind
from tigrbl_identity_model_bases import IdentityBase, required_text


@dataclass(frozen=True, slots=True, kw_only=True)
class MachineIdentity(IdentityBase):
    id: str = ""
    subject: str = ""
    kind: PrincipalKind = field(default=PrincipalKind.MACHINE_IDENTITY, init=False)
    subject_id: str = ""
    owner_id: str = ""
    credential_id: str = ""
    credential_rotates_at: datetime | None = None
    allowed_audiences: frozenset[str] = field(default_factory=frozenset)
    human: bool = False

    def __post_init__(self) -> None:
        subject_id = required_text(
            self.subject_id or self.subject or self.id, "subject id"
        )
        object.__setattr__(self, "subject_id", subject_id)
        object.__setattr__(self, "id", self.id or subject_id)
        object.__setattr__(self, "subject", self.subject or subject_id)
        object.__setattr__(self, "allowed_audiences", frozenset(self.allowed_audiences))
        IdentityBase.__post_init__(self)


__all__ = ["MachineIdentity"]
