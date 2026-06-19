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


__all__ = ["PrincipalKind", "PrincipalStatus"]
