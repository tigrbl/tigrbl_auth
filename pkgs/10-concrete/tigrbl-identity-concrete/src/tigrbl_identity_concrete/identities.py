from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Iterable
from uuid import uuid4

from tigrbl_identity_contracts.authority import AuthorityRole
from tigrbl_identity_contracts.principals import Identity, PrincipalKind, PrincipalStatus


def _new_identity_id() -> str:
    return str(uuid4())


def _required_text(value: str, field_name: str) -> str:
    cleaned = str(value).strip()
    if not cleaned:
        raise ValueError(f"{field_name} is required")
    return cleaned


def _clean_tuple(values: Iterable[str] = ()) -> tuple[str, ...]:
    return tuple(sorted({str(value).strip() for value in values if str(value).strip()}))


@dataclass(frozen=True, slots=True, kw_only=True)
class UserIdentity(Identity):
    id: str = field(default_factory=_new_identity_id)
    kind: PrincipalKind = field(default=PrincipalKind.USER, init=False)


@dataclass(frozen=True, slots=True, kw_only=True)
class AdminIdentity(Identity):
    id: str = field(default_factory=_new_identity_id)
    kind: PrincipalKind = field(default=PrincipalKind.USER, init=False)

    def __post_init__(self) -> None:
        roles = {AuthorityRole.ADMIN.value, *self.roles}
        object.__setattr__(self, "roles", tuple(sorted(roles)))
        Identity.__post_init__(self)


@dataclass(frozen=True, slots=True, kw_only=True)
class ServiceIdentity(Identity):
    id: str = ""
    subject: str = ""
    kind: PrincipalKind = field(default=PrincipalKind.SERVICE_IDENTITY, init=False)
    service_id: str = ""
    name: str = ""
    scopes: tuple[str, ...] = ()
    enabled: bool = True

    def __post_init__(self) -> None:
        service_id = _required_text(self.service_id or self.subject or self.id, "service id")
        object.__setattr__(self, "service_id", service_id)
        object.__setattr__(self, "id", self.id or service_id)
        object.__setattr__(self, "subject", self.subject or f"service:{service_id}")
        object.__setattr__(self, "name", self.name or self.display_name or service_id)
        object.__setattr__(self, "display_name", self.display_name or self.name)
        object.__setattr__(self, "scopes", _clean_tuple(self.scopes))
        if not self.enabled:
            object.__setattr__(self, "status", PrincipalStatus.DISABLED)
        Identity.__post_init__(self)


@dataclass(frozen=True, slots=True, kw_only=True)
class ClientIdentity(Identity):
    id: str = field(default_factory=_new_identity_id)
    kind: PrincipalKind = field(default=PrincipalKind.CLIENT_IDENTITY, init=False)


@dataclass(frozen=True, slots=True, kw_only=True)
class MachineIdentity(Identity):
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
        subject_id = _required_text(self.subject_id or self.subject or self.id, "subject id")
        object.__setattr__(self, "subject_id", subject_id)
        object.__setattr__(self, "id", self.id or subject_id)
        object.__setattr__(self, "subject", self.subject or subject_id)
        object.__setattr__(self, "allowed_audiences", frozenset(self.allowed_audiences))
        Identity.__post_init__(self)


@dataclass(frozen=True, slots=True, kw_only=True)
class WorkloadIdentity(Identity):
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
        workload_id = _required_text(self.workload_id or self.subject or self.id, "workload id")
        object.__setattr__(self, "workload_id", workload_id)
        object.__setattr__(self, "id", self.id or workload_id)
        object.__setattr__(self, "subject", self.subject or f"workload:{workload_id}")
        if self.revoked:
            object.__setattr__(self, "status", PrincipalStatus.DISABLED)
        Identity.__post_init__(self)


@dataclass(frozen=True, slots=True, kw_only=True)
class DeviceIdentity(Identity):
    id: str = ""
    subject: str = ""
    kind: PrincipalKind = field(default=PrincipalKind.DEVICE_IDENTITY, init=False)
    device_id: str = ""
    subject_id: str = ""
    credential_posture: str = ""
    last_ip_country: str | None = None
    created_at: str = ""
    revoked: bool = False

    def __post_init__(self) -> None:
        device_id = _required_text(self.device_id or self.id or self.subject, "device id")
        subject_id = _required_text(self.subject_id or self.subject or device_id, "subject id")
        object.__setattr__(self, "device_id", device_id)
        object.__setattr__(self, "subject_id", subject_id)
        object.__setattr__(self, "id", self.id or device_id)
        object.__setattr__(self, "subject", self.subject or subject_id)
        if self.revoked:
            object.__setattr__(self, "status", PrincipalStatus.DISABLED)
        Identity.__post_init__(self)


__all__ = [
    "AdminIdentity",
    "ClientIdentity",
    "DeviceIdentity",
    "MachineIdentity",
    "ServiceIdentity",
    "UserIdentity",
    "WorkloadIdentity",
]
