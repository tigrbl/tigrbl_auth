from __future__ import annotations

"""Projection metadata for identity contract documents.

Request and response schemas are owned by the storage table modules that expose
the corresponding custom operations.
"""

from dataclasses import dataclass, field
from typing import Any, Literal


@dataclass(frozen=True, slots=True)
class ContractProjection:
    kind: Literal["openapi"]
    profile: str
    version: str
    document: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.kind != "openapi":
            raise ValueError("ContractProjection.kind must be 'openapi'")


__all__ = ["ContractProjection"]
