"""Policy kind contract enums."""

from __future__ import annotations

from enum import Enum


class PolicyKind(str, Enum):
    RBAC = "rbac"
    ABAC = "abac"
    PBAC = "pbac"
    DELEGATION = "delegation"
    ADMIN = "admin"


__all__ = ["PolicyKind"]
