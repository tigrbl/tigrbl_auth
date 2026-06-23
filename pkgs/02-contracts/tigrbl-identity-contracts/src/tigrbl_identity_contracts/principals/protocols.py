from __future__ import annotations

from typing import Protocol, runtime_checkable

from tigrbl_identity_core.typing import StrUUID


@runtime_checkable
class PrincipalLike(Protocol):
    """Minimum principal surface required by authentication helpers."""

    id: StrUUID
    tenant_id: StrUUID


__all__ = ["PrincipalLike"]
