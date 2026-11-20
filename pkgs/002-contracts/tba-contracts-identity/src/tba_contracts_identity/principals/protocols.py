from __future__ import annotations

from typing import Protocol, runtime_checkable

from tba_primitives_identity.typing import StrUUID


@runtime_checkable
class PrincipalLike(Protocol):
    """Minimum principal surface required by authentication helpers."""

    id: StrUUID
    tenant_id: StrUUID


__all__ = ["PrincipalLike"]
