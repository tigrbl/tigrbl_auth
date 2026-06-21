"""Policy effect contract enums."""

from __future__ import annotations

from enum import Enum


class DecisionEffect(str, Enum):
    ALLOW = "allow"
    DENY = "deny"


__all__ = ["DecisionEffect"]
