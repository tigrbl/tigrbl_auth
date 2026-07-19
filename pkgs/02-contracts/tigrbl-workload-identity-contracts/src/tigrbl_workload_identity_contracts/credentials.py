"""Protocol-neutral workload credential requests and results."""

from dataclasses import dataclass
from datetime import datetime

from tigrbl_identity_core import CredentialFormat, TrustMaterialId, WorkloadCredentialId

from .identity import WorkloadIdentityRef
from .references import WorkloadReference


@dataclass(frozen=True, slots=True)
class WorkloadCredentialRequest:
    workload: WorkloadReference
    credential_format: CredentialFormat
    audience: tuple[str, ...] = ()
    requested_identity: WorkloadIdentityRef | None = None

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "credential_format",
            CredentialFormat(self.credential_format),
        )
        object.__setattr__(self, "audience", tuple(self.audience))


@dataclass(frozen=True, slots=True)
class WorkloadCredential:
    credential_id: WorkloadCredentialId
    identity: WorkloadIdentityRef
    format: CredentialFormat
    artifact: bytes | str
    valid_until: datetime | None = None
    trust_material_ref: TrustMaterialId | None = None

    def __post_init__(self) -> None:
        object.__setattr__(self, "format", CredentialFormat(self.format))


@dataclass(frozen=True, slots=True)
class WorkloadCredentialSet:
    credentials: tuple[WorkloadCredential, ...]
    version: str

    def __post_init__(self) -> None:
        object.__setattr__(self, "credentials", tuple(self.credentials))
        if not self.version:
            raise ValueError("credential-set version is required")


__all__ = ["WorkloadCredential", "WorkloadCredentialRequest", "WorkloadCredentialSet"]