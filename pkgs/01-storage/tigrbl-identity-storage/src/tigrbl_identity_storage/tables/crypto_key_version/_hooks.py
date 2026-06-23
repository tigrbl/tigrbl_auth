"""Storage-owned crypto key version response hooks."""

from __future__ import annotations

from typing import Any

_JWK_SECRET_FIELDS = {"d", "p", "q", "dp", "dq", "qi"}


def _scrub_public_material(material: Any) -> Any:
    if isinstance(material, dict):
        return {key: value for key, value in material.items() if key not in _JWK_SECRET_FIELDS}
    return material


def scrub_key_version_material(payload: Any) -> Any:
    if isinstance(payload, dict):
        cleaned = dict(payload)
        cleaned.pop("provider_key_ref", None)
        cleaned["public_material"] = _scrub_public_material(cleaned.get("public_material"))
        return cleaned
    if hasattr(payload, "provider_key_ref"):
        try:
            setattr(payload, "provider_key_ref", None)
        except Exception:
            pass
    if hasattr(payload, "public_material"):
        try:
            setattr(payload, "public_material", _scrub_public_material(getattr(payload, "public_material")))
        except Exception:
            pass
    return payload


__all__ = ["scrub_key_version_material"]
