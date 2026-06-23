"""Storage-owned key version response hooks."""

from __future__ import annotations

from typing import Any


def scrub_key_version_material(payload: Any) -> Any:
    if isinstance(payload, dict):
        cleaned = dict(payload)
        cleaned.pop("provider_key_ref", None)
        jwk = cleaned.get("public_jwk")
        if isinstance(jwk, dict):
            cleaned["public_jwk"] = {key: value for key, value in jwk.items() if key not in {"d", "p", "q", "dp", "dq", "qi"}}
        return cleaned
    if hasattr(payload, "provider_key_ref"):
        try:
            setattr(payload, "provider_key_ref", None)
        except Exception:
            pass
    return payload


__all__ = ["scrub_key_version_material"]
