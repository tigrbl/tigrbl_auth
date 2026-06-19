from __future__ import annotations

from enum import Enum


class JoseKeyStatus(str, Enum):
    ACTIVE = "active"
    NEXT = "next"
    RETIRED = "retired"
    DISABLED = "disabled"


class JoseKeyUse(str, Enum):
    SIGN = "sig"
    ENCRYPT = "enc"


__all__ = ["JoseKeyStatus", "JoseKeyUse"]
