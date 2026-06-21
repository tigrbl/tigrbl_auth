from __future__ import annotations

from enum import Enum


class PrincipalKind(str, Enum):
    USER = "user"
    ADMIN = "admin"
    SERVICE = "service"
    APP = "app"
    MACHINE = "machine"
    WORKLOAD = "workload"
    DEVICE = "device"


class PrincipalStatus(str, Enum):
    ACTIVE = "active"
    DISABLED = "disabled"
    LOCKED = "locked"
    DELETED = "deleted"


NONHUMAN_PRINCIPAL_KINDS = frozenset(
    {
        PrincipalKind.SERVICE,
        PrincipalKind.APP,
        PrincipalKind.MACHINE,
        PrincipalKind.WORKLOAD,
        PrincipalKind.DEVICE,
    }
)


__all__ = [
    "NONHUMAN_PRINCIPAL_KINDS",
    "PrincipalKind",
    "PrincipalStatus",
]
