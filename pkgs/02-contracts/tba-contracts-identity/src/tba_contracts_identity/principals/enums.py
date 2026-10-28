from __future__ import annotations

from enum import Enum


class PrincipalKind(str, Enum):
    USER = "user"
    SERVICE_IDENTITY = "service_identity"
    MACHINE_IDENTITY = "machine_identity"
    WORKLOAD_IDENTITY = "workload_identity"
    CLIENT_IDENTITY = "client_identity"
    EXTERNAL_SUBJECT = "external_subject"
    DEVICE_IDENTITY = "device_identity"


class PrincipalStatus(str, Enum):
    ACTIVE = "active"
    DISABLED = "disabled"
    LOCKED = "locked"
    DELETED = "deleted"


NONHUMAN_PRINCIPAL_KINDS = frozenset(
    {
        PrincipalKind.SERVICE_IDENTITY,
        PrincipalKind.MACHINE_IDENTITY,
        PrincipalKind.WORKLOAD_IDENTITY,
        PrincipalKind.CLIENT_IDENTITY,
        PrincipalKind.EXTERNAL_SUBJECT,
        PrincipalKind.DEVICE_IDENTITY,
    }
)


__all__ = [
    "NONHUMAN_PRINCIPAL_KINDS",
    "PrincipalKind",
    "PrincipalStatus",
]
