"""CWT claim-map migration entry point."""

from typing import Any, Mapping

from .versions import CURRENT_VERSION


def migrate_claims(
    value: Mapping[str | int, Any],
    *,
    source: str,
    target: str = CURRENT_VERSION.value,
) -> dict[str | int, Any]:
    if source != CURRENT_VERSION.value or target != CURRENT_VERSION.value:
        raise ValueError(f"unsupported CWT migration: {source} -> {target}")
    return dict(value)


__all__ = ["migrate_claims"]
