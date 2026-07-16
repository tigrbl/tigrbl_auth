from dataclasses import dataclass, field
from tigrbl_identity_contracts.principals import PrincipalKind, PrincipalStatus
from tigrbl_identity_bases import IdentityBase
from tigrbl_identity_core import required_text


@dataclass(frozen=True, slots=True, kw_only=True)
class WorkloadIdentity(IdentityBase):
    id: str = ""
    subject: str = ""
    kind: PrincipalKind = field(default=PrincipalKind.WORKLOAD_IDENTITY, init=False)
    workload_id: str = ""
    trust_domain: str = ""
    cloud: str = ""
    namespace: str = ""
    attestor: str = ""
    credential_id: str = ""
    created_at: str = ""
    revoked: bool = False

    def __post_init__(self) -> None:
        workload_id = required_text(
            self.workload_id or self.subject or self.id, "workload id"
        )
        object.__setattr__(self, "workload_id", workload_id)
        object.__setattr__(self, "id", self.id or workload_id)
        object.__setattr__(self, "subject", self.subject or f"workload:{workload_id}")
        if self.revoked:
            object.__setattr__(self, "status", PrincipalStatus.DISABLED)
        IdentityBase.__post_init__(self)


__all__ = ["WorkloadIdentity"]
