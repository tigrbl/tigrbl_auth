"""Policy request contract dataclasses."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping


@dataclass(frozen=True, slots=True)
class PolicyRequest:
    subject: str
    tenant_id: str
    action: str
    resource: str = ""
    roles: tuple[str, ...] = ()
    attributes: Mapping[str, Any] = field(default_factory=dict)
    permissions: tuple[str, ...] = ()
    delegated_by: str | None = None
    admin: bool = False


__all__ = ["PolicyRequest"]
