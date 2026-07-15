"""Protected-resource verifier-metadata migration paths."""

from typing import Any, Mapping

from .versions import CURRENT_VERSION


def migrate_verifier_metadata(
    value: Mapping[str, Any],
    *,
    source: str,
    target: str = CURRENT_VERSION.identifier,
) -> dict[str, Any]:
    if source == target:
        return dict(value)
    if source != "legacy-unversioned" or target != CURRENT_VERSION.identifier:
        raise ValueError(
            f"unsupported protected-resource migration: {source} -> {target}"
        )
    # Existing verifier metadata already uses the profile's stable wire names.
    # Version selection stays outside the protocol payload.
    return dict(value)


__all__ = ["migrate_verifier_metadata"]
